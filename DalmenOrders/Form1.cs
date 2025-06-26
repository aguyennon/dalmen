using System;
using System.Collections.Generic;
using System.Data;
using System.Data.OleDb;
using System.IO;
using System.Linq;
using System.Text;
using System.Windows.Forms;

namespace DalmenOrders
{

    public partial class Form1 : Form
    {
        private const double KERF = 4.0; // Measurements all in mm
        public Form1()
        {
            InitializeComponent();
        }


        private void btnOptimize_Click(object sender, EventArgs e)
        {
            // Array to hold cut quantity + cut length values inputted
            List<int> cutQtys = new List<int>();
            List<double> cutLengths = new List<double>();
            List<CutItem> cutItems = new List<CutItem>();

            try
            {
                // Collect values from tbxCutQTY1 thru tbxCutQTY9 and tbxCutLength1 thru tbxCutLength9 
                for (int i = 1; i <= 12; i++)
                {
                    TextBox qtyBox = (TextBox)this.Controls.Find("tbxCutQTY" + i, true).FirstOrDefault();
                    TextBox lenBox = (TextBox)this.Controls.Find("tbxCutLength" + i, true).FirstOrDefault();

                    if (qtyBox != null && lenBox != null)
                    {
                        if (!string.IsNullOrWhiteSpace(qtyBox.Text) && !string.IsNullOrWhiteSpace(lenBox.Text))
                        {
                            int qty = int.Parse(qtyBox.Text);
                            double len = double.Parse(lenBox.Text);

                            if (qty < 0 || len < 0)
                            {
                                MessageBox.Show("All values must be positive.");
                                return;
                            }

                            cutItems.Add(new CutItem { Quantity = qty, Length = len });
                        }
                    }
                }

                if (cutItems.Count == 0)
                {
                    MessageBox.Show("Please enter at least one cut quantity and length.");
                    return;
                }
            }
            catch (FormatException)
            {   // will need to leave exception for Lot
                MessageBox.Show("All inputs must only be numeric.");
            }
            // How much stock there is
            int stockQty = 0;
            // How long each board is
            double stockLength = 0; // double because 2 characters since we're talking about length here

            if (!double.TryParse(tbxStockLength.Text, out stockLength) || stockLength <= 0)
            {
                MessageBox.Show("Stock Length must be a positive number.");
                return;
            }

            if (!int.TryParse(tbxStockQTY.Text, out stockQty) || stockQty <= 0)
            {
                MessageBox.Show("Stock Quantity must be a positive number.");
                return;
            }

            // List created to keep track of all cut lengths
            List<double> allCuts = new List<double>();
            for (int i = 0; i < cutQtys.Count; i++)
            {
                for (int j = 0; j < cutQtys[i]; j++)
                {
                    allCuts.Add(cutLengths[i]);
                }
            }

            // To sort cuts in descending order aka longest first etc.
            allCuts.Sort((a, b) => b.CompareTo(a));

            // Sort cut items by length descending (just like VBA)
            cutItems = cutItems.OrderByDescending(x => x.Length).ToList();

            if (allCuts.Count > 0 && (allCuts[0] + KERF) > stockLength)
            {
                MessageBox.Show("At least one cut including the kerf, is greater than stock length.");
                return;
            }

            var primaryResult = OptimizeStock(cutItems, stockLength, stockQty);

            if (!primaryResult.IsSuccess)
            {
                MessageBox.Show(primaryResult.ErrorMsg);
                return;
            }

            string primaryDelignage = tbxDeligne.Text.Trim();
            string secondaryDelignage = tbxDeligne2.Text.Trim();

            OptimizationResult secondaryResult = null;
            if (!string.IsNullOrEmpty(secondaryDelignage) && secondaryDelignage != primaryDelignage)
            {
                // Try to optimize with secondary delignage
                secondaryResult = OptimizeStock(cutItems, stockLength, stockQty);
                if (!secondaryResult.IsSuccess)
                {
                    MessageBox.Show(secondaryResult.ErrorMsg);
                    return;
                }

                Form2 results_Form = new Form2(primaryResult, secondaryResult, tbxLotNumber.Text, primaryDelignage, secondaryDelignage);
                results_Form.ShowDialog();
            }

            List<List<double>> boardCuts = new List<List<double>>(); // stores cuts per board
            List<double> boardWaste = new List<double>(); // stores waste/remaining length

            // Logic
            var result = OptimizeStock(cutItems, stockLength, stockQty);

            if (!result.IsSuccess)
            {
                MessageBox.Show(result.ErrorMsg);
                return;
            }

            // Format and display results matching VBA output
            StringBuilder output = new StringBuilder();
            output.AppendLine("DÉLIGNÉ À: " + tbxDeligne.Text);
            output.AppendLine("Lot #: " + tbxLotNumber.Text);
            output.AppendLine("Total Boards = " + result.TotalBoards);
            output.AppendLine();
            output.AppendLine("Board No.\tStock Length\tCut Length");

            foreach (var usage in result.Usage)
            {
                string cutDisplay = usage.IsWaste ? usage.CutLength + " Waste" : usage.CutLength.ToString();
                output.AppendLine($"{usage.BoardNumber}\t\t{usage.StockLength}\t\t{cutDisplay}");
            }

            output.AppendLine();
            output.AppendLine("Total Waste: " + result.TotalWaste);

            List<string> delignageValues = new List<string>();
            if (!string.IsNullOrEmpty(tbxDeligne.Text))
                delignageValues.Add(tbxDeligne.Text.Trim());
            if (!string.IsNullOrEmpty(tbxDeligne2.Text))
                delignageValues.Add(tbxDeligne2.Text.Trim());

            if (delignageValues.Count == 0)
                delignageValues.Add("");

            MultiDelignageResult multiResult = new MultiDelignageResult
            {
                LotNumber = tbxLotNumber.Text
            };

            foreach (string delignage in delignageValues)
            {
                var result_ = OptimizeStock(cutItems, stockLength, stockQty);

                if (result_.IsSuccess)  // Changed from !result_.IsSuccess
                {
                    multiResult.DelignageResults.Add(new DelignageOptimizationResult
                    {
                        DelignageValue = delignage,
                        OptimizationResult = result_,
                        CutsForThisDelignage = cutItems.ToList()
                    });
                }
                else
                {
                    MessageBox.Show($"Error optimizing for delignage '{delignage}': {result_.ErrorMsg}");
                    return;
                }
            }

            // Important to load Form2
            Form2 resultsForm = new Form2(result, tbxLotNumber.Text, tbxDeligne.Text);
            resultsForm.ShowDialog();
        }
        private OptimizationResult OptimizeStock(List<CutItem> cutItems, double stockLength, int stockQty)
        {
            var result = new OptimizationResult { IsSuccess = true };
            var workingCuts = cutItems.Select(c => new CutItem { Quantity = c.Quantity, Length = c.Length }).ToList();

            double totalWaste = 0;
            int totalBoards = 0;
            int stockRemaining = stockQty;
            double currentBoardRemaining = 0;
            bool needNewBoard = true;

            while (workingCuts.Any(c => c.Quantity > 0))
            {
                double minCut = workingCuts.Where(c => c.Quantity > 0).Min(c => c.Length);

                if (needNewBoard)
                {
                    if (stockRemaining <= 0)
                    {
                        result.IsSuccess = false;
                        result.ErrorMsg = "Not enough Stock to make all Pieces at Cut Lengths!!!";
                        return result;
                    }
                    totalBoards++;
                    currentBoardRemaining = stockLength;
                    stockRemaining--;
                    needNewBoard = false;
                }

                bool madeCut = false;
                while (currentBoardRemaining >= (minCut + KERF) && workingCuts.Any(c => c.Quantity > 0))
                {
                    var cutToMake = workingCuts.Where(c => c.Quantity > 0 && (c.Length + KERF) <= currentBoardRemaining)
                                              .OrderByDescending(c => c.Length)
                                              .FirstOrDefault();

                    if (cutToMake != null)
                    {
                        result.Usage.Add(new StockUsage
                        {
                            BoardNumber = totalBoards,
                            StockLength = stockLength,
                            CutLength = cutToMake.Length,
                            IsWaste = false
                        });

                        currentBoardRemaining -= (cutToMake.Length + KERF);
                        cutToMake.Quantity--;
                        madeCut = true;
                    }
                    else
                    {
                        break;
                    }

                    minCut = workingCuts.Where(c => c.Quantity > 0).Any() ?
                             workingCuts.Where(c => c.Quantity > 0).Min(c => c.Length) : 0;
                }

                if (currentBoardRemaining > 0 && !madeCut)
                {
                    totalWaste += currentBoardRemaining;
                    result.Usage.Add(new StockUsage
                    {
                        BoardNumber = totalBoards,
                        StockLength = stockLength,
                        CutLength = currentBoardRemaining,
                        IsWaste = true
                    });
                    needNewBoard = true;
                }
                else if (currentBoardRemaining == 0 || !workingCuts.Any(c => c.Quantity > 0 && (c.Length + KERF) <= currentBoardRemaining))
                {
                    if (currentBoardRemaining > 0)
                    {
                        totalWaste += currentBoardRemaining;
                        result.Usage.Add(new StockUsage
                        {
                            BoardNumber = totalBoards,
                            StockLength = stockLength,
                            CutLength = currentBoardRemaining,
                            IsWaste = true
                        });
                    }
                    needNewBoard = true;
                }
            }

            result.TotalBoards = totalBoards;
            result.TotalWaste = totalWaste;
            return result;
        }

        public void LoadProcessedCuts(List<CutItem> processedCuts)
        {
            try
            {
                ClearAllCutInputs();

                int maxCuts = Math.Min(processedCuts.Count, 12); // Limit to 12 cuts

                for (int i = 0; i < maxCuts; i++)
                {
                    int textboxIndex = i + 1; // Textboxes are numbered 1-12

                    TextBox qtyBox = (TextBox)this.Controls.Find("tbxCutQTY" + textboxIndex, true).FirstOrDefault();
                    TextBox lenBox = (TextBox)this.Controls.Find("tbxCutLength" + textboxIndex, true).FirstOrDefault();

                    if (qtyBox != null && lenBox != null)
                    {
                        qtyBox.Text = processedCuts[i].Quantity.ToString();
                        lenBox.Text = processedCuts[i].Length.ToString();
                    }
                }

                // If there are more than 12 unique cuts, show a warning
                if (processedCuts.Count > 12)
                {
                    MessageBox.Show($"You have {processedCuts.Count} unique cuts, but only the first 12 have been loaded. " +
                                  "The remaining cuts are:\n" +
                                  string.Join("\n", processedCuts.Skip(12).Select(c => $"Length: {c.Length}, Qty: {c.Quantity}")),
                                  "Too Many Cuts", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                }

            
                MessageBox.Show($"Successfully loaded {maxCuts} cut lengths into the optimizer!",
                               "Cuts Loaded", MessageBoxButtons.OK, MessageBoxIcon.Information);
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Error loading processed cuts: {ex.Message}", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void HandleProcessedCuts(List<CutItem> processedCuts)
        {
            if (processedCuts == null || processedCuts.Count == 0)
            {
                MessageBox.Show("No valid cuts to process.");
                return;
            }

            // Clear all 12 sets first
            for (int i = 1; i <= 12; i++)
            {
                TextBox qtyBox = (TextBox)this.Controls.Find("tbxCutQTY" + i, true).FirstOrDefault();
                TextBox lenBox = (TextBox)this.Controls.Find("tbxCutLength" + i, true).FirstOrDefault();

                if (qtyBox != null) qtyBox.Clear();
                if (lenBox != null) lenBox.Clear();
            }

            // Populate with new values
            for (int i = 0; i < processedCuts.Count && i < 12; i++)
            {
                TextBox qtyBox = (TextBox)this.Controls.Find("tbxCutQTY" + (i + 1), true).FirstOrDefault();
                TextBox lenBox = (TextBox)this.Controls.Find("tbxCutLength" + (i + 1), true).FirstOrDefault();

                if (qtyBox != null) qtyBox.Text = processedCuts[i].Quantity.ToString();
                if (lenBox != null) lenBox.Text = processedCuts[i].Length.ToString();
            }
        }

        private void ClearAllCutInputs()
        {
            for (int i = 1; i <= 12; i++)
            {
                TextBox qtyBox = (TextBox)this.Controls.Find("tbxCutQTY" + i, true).FirstOrDefault();
                TextBox lenBox = (TextBox)this.Controls.Find("tbxCutLength" + i, true).FirstOrDefault();
                if (qtyBox != null) qtyBox.Clear();
                if (lenBox != null) lenBox.Clear();
            }
        }

        private void btnExit_Click(object sender, EventArgs e)
        {
            Application.Exit();
        }

        private void Form1_Load(object sender, EventArgs e)
        {

        }

        private void btnOpen_Click(object sender, EventArgs e)
        {
            string lotNumber = tbxLotNumber.Text.Trim();
            if (string.IsNullOrEmpty(lotNumber))
            {
                MessageBox.Show("Please enter a Lot Number.");
                return;
            }

            string dbPath = Path.Combine(@"Q:\Quotes\FichierDeScie\Soufflage", lotNumber + ".mdb");

            if (!File.Exists(dbPath))
            {
                MessageBox.Show($"Database for Lot #{lotNumber} not found in Q:\\Quotes\\FichierDeScie\\Soufflage\\");
                return;
            }

            List<CutItem> loadedCuts = new List<CutItem>();
            List<string> delignageValues = new List<string>();

            try
            {
                string connStr = $@"Provider=Microsoft.Jet.OLEDB.4.0;Data Source={dbPath};Persist Security Info=False;";
                using (OleDbConnection conn = new OleDbConnection(connStr))
                {
                    conn.Open();
                    using (OleDbCommand cmd = new OleDbCommand("SELECT Taille, POS_1 FROM Soufflage ORDER BY IDENTIF, LIGNE", conn)) // need POS_1
                    using (OleDbDataReader reader = cmd.ExecuteReader())
                    {
                        while (reader.Read())
                        {
                            if (!reader.IsDBNull(0))
                            {
                                double len = Convert.ToDouble(reader["Taille"]);
                                string delignage = reader.IsDBNull(1) ? "" : reader["POS_1"].ToString();

                                loadedCuts.Add(new CutItem { Quantity = 1, Length = len }); 
                                delignageValues.Add(delignage);
                            }
                        }
                    }
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show("Error loading data from database:\n" + ex.Message);
                return;
            }

            var delignageGroups = delignageValues.GroupBy(d => d)
                .Select(g => new { Delignage = g.Key, Count = g.Count() })
                .OrderByDescending(g => g.Count)
                .ToList();

            StringBuilder delignageInfo = new StringBuilder();
            delignageInfo.AppendLine("Delignage Values Found:");

            foreach (var group in delignageGroups)
            {
                delignageInfo.AppendLine($"- {group.Delignage}: {group.Count} pieces");
            }

            if (delignageGroups.Count >= 1)
            {
                tbxDeligne.Text = delignageGroups[0].Delignage;


                if (delignageGroups.Count > 1)
                {
                    tbxDeligne2.Text = delignageGroups[1].Delignage;

                    delignageInfo.AppendLine();
                    delignageInfo.AppendLine($"Primary delignage '{delignageGroups[0].Delignage}' tbxDeligne");
                    delignageInfo.AppendLine($"Secondary delignage '{delignageGroups[1].Delignage}' tbxDeligne2");
                }
                else
                {
                    tbxDeligne2.Clear();
                }
            }
            else
            {
                tbxDeligne.Clear();
                tbxDeligne2.Clear();
            }


                using (InputForm inputForm = new InputForm())
                {
                    inputForm.ProcessedCuts = loadedCuts;
                    inputForm.DataProcessed = true;
                    inputForm.InitializeCuts();

                var result = inputForm.ShowDialog();

                if (result == DialogResult.OK)
                {
                    if (inputForm.ProcessedCuts != null && inputForm.ProcessedCuts.Count > 0)
                    {
                        HandleProcessedCuts(inputForm.ProcessedCuts);
                    }
                }
               

            }
        }

        private void Form1_FormClosing(object sender, FormClosingEventArgs e)
        {
            Application.Exit(); // Ensure application exits cleanly
        }
    }
}