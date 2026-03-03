using System;
using System.Collections.Generic;
using System.Data;
using System.Data.OleDb;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Text;
using System.Windows.Forms;

namespace DalmenOrders
{

    public partial class Form1 : Form
    {
        // KERF needed, it's the saw blade width that is removed from the stock length for each cut.
        private const double KERF = 4.0; // Measurements all in mm
        public Form1()
        {
            InitializeComponent();
            tbxLotNumber.TextChanged += tbxLotNumber_TextChanged;
        }


        #region Optimization Click event
        // Settings for when the optimize button is clicked
        private void btnOptimize_Click(object sender, EventArgs e)
        {
            bool isGroupCutting = cbxTwoBoards.Checked;

            // Array to hold cut quantity + cut length values inputted
            List<CutItem> cutItems = new List<CutItem>();

            try
            {
                cutItems.Clear();
                // Collect values from tbxCutQTY1 thru tbxCutQTY14 and tbxCutLength1 thru tbxCutLength14 
                for (int i = 1; i <= 14; i++)
                {
                    TextBox qtyBox = (TextBox)this.Controls.Find("tbxCutQTY" + i, true).FirstOrDefault();
                    TextBox lenBox = (TextBox)this.Controls.Find("tbxCutLength" + i, true).FirstOrDefault();

                    if (qtyBox != null && lenBox != null)
                    {
                        // Check if both fields are filled
                        if (!string.IsNullOrWhiteSpace(qtyBox.Text) && !string.IsNullOrWhiteSpace(lenBox.Text))
                        {
                            string qtyText = qtyBox.Text.Trim();
                            string lenText = lenBox.Text.Trim();

                            if (!string.IsNullOrEmpty(qtyText) && !string.IsNullOrEmpty(lenText))
                            {
                                int qty = int.Parse(qtyText);
                                double len = double.Parse(lenText);

                                if (qty <= 0 || len <= 0)
                                {
                                    MessageBox.Show($"All values must be positive. Check row {i}.");
                                    return;
                                }

                                cutItems.Add(new CutItem
                                {
                                    Quantity = qty,
                                    Length = len,
                                    OriginalQuantity = qty,
                                    IsGroupCut = false // Will be set when processing
                                });
                            }
                        }
                    }
                }
               
                // Check if we have any cut items - moved outside the loop
                if (cutItems.Count == 0)
                {
                    MessageBox.Show("Please enter at least one cut quantity and length.");
                    return;
                }
            }
            catch (FormatException)
            {
                MessageBox.Show("All inputs must only be numeric. Please check your entries.");
                return;
            }

            // Stock validation
            int stockQty = 0;
            double stockLength = 0;

            // Validate stock length and quantity inputs
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

            // Process cuts for group cutting if enabled
            var processedCuts = ProcessCutsForGroupCutting(cutItems, isGroupCutting);

            // Show group cutting information if enabled
            if (isGroupCutting)
            {
                //  ShowGroupCuttingInfo(cutItems, processedCuts);
            }

            // Sort cut items by length descending
            processedCuts = processedCuts.OrderByDescending(x => x.Length).ToList();

            // Check if any cut is too long
            if (processedCuts.Any(c => (c.Length + KERF) > stockLength))
            {
                MessageBox.Show("At least one cut including the kerf, is greater than stock length.");
                return;
            }

            // Get delignage numeric values from textboxes
            string primaryDelignage = tbxDeligne.Text.Trim();
            string secondaryDelignage = tbxDeligne2.Text.Trim();

            // Check if user has manual inputs - if so, prioritize them over database data
            bool hasManualInputs = HasManualInputs();

            // Use database data only if no manual inputs exist
            if (!hasManualInputs && _loadedCutsWithDelignage != null && _loadedCutsWithDelignage.Count > 0)
            {
                // Filter cuts for primary delignage
                var primaryCuts = GetCutsForDelignage(primaryDelignage);

                // Process primary cuts for group cutting
                var processedPrimaryCuts = ProcessCutsForGroupCutting(primaryCuts, isGroupCutting);

                processedPrimaryCuts = processedPrimaryCuts.OrderByDescending(x => x.Length).ToList();

                var primaryResult = OptimizeStock(processedPrimaryCuts, stockLength, stockQty);

                if (!primaryResult.IsSuccess)
                {
                    MessageBox.Show(primaryResult.ErrorMsg);
                    return;
                }

                OptimizationResult secondaryResult = null;
                if (!string.IsNullOrEmpty(secondaryDelignage) && secondaryDelignage != primaryDelignage)
                {
                    // Filter cuts for secondary delignage
                    var secondaryCuts = GetCutsForDelignage(secondaryDelignage);

                    // Process secondary cuts for group cutting
                    var processedSecondaryCuts = ProcessCutsForGroupCutting(secondaryCuts, isGroupCutting);
                    processedSecondaryCuts = processedSecondaryCuts.OrderByDescending(x => x.Length).ToList();

                    secondaryResult = OptimizeStock(processedSecondaryCuts, stockLength, stockQty);

                    if (!secondaryResult.IsSuccess)
                    {
                        MessageBox.Show(secondaryResult.ErrorMsg);
                        return;
                    }

                    // Show both results - database path
                    Form2 results_Form = new Form2(primaryResult, secondaryResult, tbxLotNumber.Text, primaryDelignage, secondaryDelignage, isGroupCutting);
                    results_Form.ShowDialog();
                    return;
                }
                else
                {
                    // Show only primary result - database path
                    Form2 resultsForm = new Form2(primaryResult, tbxLotNumber.Text, primaryDelignage, isGroupCutting);
                    resultsForm.ShowDialog();
                    return;
                }
            }
            else
            {
                // Use manual textbox inputs - this will use your cleaned cutItems list
                var result = OptimizeStock(processedCuts, stockLength, stockQty);

                if (!result.IsSuccess)
                {
                    MessageBox.Show(result.ErrorMsg);
                    return;
                }

                if (!string.IsNullOrEmpty(secondaryDelignage) && secondaryDelignage != primaryDelignage && _loadedCutsWithDelignage != null)
                {
                    var secondaryCuts = GetCutsForDelignage(secondaryDelignage);
                    var processedSecondaryCuts = ProcessCutsForGroupCutting(secondaryCuts, isGroupCutting);
                    processedSecondaryCuts = processedSecondaryCuts.OrderByDescending(x => x.Length).ToList();

                    var secondaryResult = OptimizeStock(processedSecondaryCuts, stockLength, stockQty);

                    if (!secondaryResult.IsSuccess)
                    {
                        MessageBox.Show(secondaryResult.ErrorMsg);
                    }

                    Form2 results_Form = new Form2(result, secondaryResult, tbxLotNumber.Text, primaryDelignage, secondaryDelignage, isGroupCutting);
                    results_Form.ShowDialog();
                }
                else
                {
                    ShowOptimizationSummary(result, isGroupCutting);

                    Form2 resultsForm = new Form2(result, tbxLotNumber.Text, primaryDelignage, isGroupCutting);
                    resultsForm.ShowDialog();
                }   
            }
        }

        List<CutItem> GetCutsForDelignage(string delignage)
        {
            var cuts = _loadedCutsWithDelignage
                .Where(c => c.Delignage == delignage)
                .GroupBy(c => c.Length)
                .Select(g => new CutItem
                {
                    Length = g.Key,
                    Quantity = g.Count(),
                    OriginalQuantity = g.Count(),
                    IsGroupCut = false
                })
                .ToList();

            if (cuts.Count == 0)
            {
                cuts = _loadedCutsWithDelignage

                    .GroupBy(c => c.Length)
                    .Select(g => new CutItem
                    {
                        Length = g.Key,
                        Quantity = g.Count(),
                        OriginalQuantity = g.Count(),
                        IsGroupCut = false
                    })
                    .ToList();
            }
            return cuts;
        }

        private bool HasManualInputs()
        {
            for (int i = 1; i <= 14; i++)
            {
                TextBox qtyBox = (TextBox)this.Controls.Find("tbxCutQTY" + i, true).FirstOrDefault();
                TextBox lenBox = (TextBox)this.Controls.Find("tbxCutLength" + i, true).FirstOrDefault();
                if (qtyBox != null && lenBox != null)
                {
                    if (!string.IsNullOrWhiteSpace(qtyBox.Text) && !string.IsNullOrWhiteSpace(lenBox.Text))
                    {
                        return true;
                    }
                }
            }
            return false;
        }

        private void ShowOptimizationSummary(OptimizationResult result, bool isGroupCutting = false)
        {
            StringBuilder summary = new StringBuilder("Optimization Complete!\n\n");

            if (isGroupCutting)
            {
                summary.AppendLine("Group Cutting Mode: Cutting 2 boards at once");
                summary.AppendLine();
            }

            summary.AppendLine($"Total Boards Used: {result.TotalBoards}");
            if (isGroupCutting)
            {
                summary.AppendLine($"(Each board cut produces pieces from 2 boards)");
            }
            summary.AppendLine($"Total Waste: {result.TotalWaste:F1}mm");

            MessageBox.Show(summary.ToString(), "Optimization Results", MessageBoxButtons.OK, MessageBoxIcon.Information);
        }
        #endregion

        #region Extra GetterAndSetter Added
        // Class to hold cut items with delignage information
        public class CutItemWithDelignage : CutItem
        {
            public string Delignage { get; set; }
            public double Lengths { get; set; }
        }
        #endregion

        #region Optimization Results & Functionality
        // List to hold loaded cuts with delignage information
        private List<CutItemWithDelignage> _loadedCutsWithDelignage;
        private OptimizationResult OptimizeStock(List<CutItem> cutItems, double stockLength, int stockQty)
        {
            var result = new OptimizationResult { IsSuccess = true };
            var workingCuts = cutItems.Select(c => new CutItem { Quantity = c.Quantity, Length = c.Length }).ToList();

            double totalWaste = 0;
            int totalBoards = 0;
            int stockRemaining = stockQty;
            double currentBoardRemaining = 0;
            bool needNewBoard = true;

            // While there are still cuts to make, continue processing
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

                // If the current board remaining length is less than the minimum cut length, we need a new board
                bool madeCut = false;
                while (currentBoardRemaining >= (minCut + KERF) && workingCuts.Any(c => c.Quantity > 0))
                {
                    var cutToMake = workingCuts.Where(c => c.Quantity > 0 && (c.Length + KERF) <= currentBoardRemaining)
                                              .OrderByDescending(c => c.Length)
                                              .FirstOrDefault();
                    // If we found a cut that can be made
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
                // If we made cuts but still have remaining length on the board thats added in the total waste
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
                // If we didn't make any cuts and the current board remaining is 0 or no cuts can be made, we need a new board
                else if (currentBoardRemaining == 0 || !workingCuts.Any(c => c.Quantity > 0 && (c.Length + KERF) <= currentBoardRemaining))
                {
                    // If we have remaining length on the current board, add it to the total waste
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
        #endregion

        #region Processed Cuts
        // Method to load processed cuts into the textboxes
        public void LoadProcessedCuts(List<CutItem> processedCuts)
        {
            try
            {
                ClearAllCutInputs();

                // Limit to 12 cuts because only have 12 textboxes for it ( could be customized later on to  fit more data..?
                int maxCuts = Math.Min(processedCuts.Count, 12);
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

        // Method to handle processed cuts from the InputForm
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
        #endregion

        #region Click Events (Exit, Open, etc.)
        // Method to exit the application when the exit button is clicked
        private void btnExit_Click(object sender, EventArgs e)
        {
            Application.Exit();
        }

        // Method to open the database and load cuts based on the lot number entered
        private void btnOpen_Click(object sender, EventArgs e)
        {
            string lotNumber = tbxLotNumber.Text.Trim();
            if (string.IsNullOrEmpty(lotNumber))
            {
                MessageBox.Show("Please enter a Lot Number.");
                return;
            }

            // Constructor for the database path again 
            string dbPath = Path.Combine(@"Q:\Quotes\FichierDeScie\Soufflage", lotNumber + ".mdb");

            // If the path doesnt work or the number entered isn't valid, show an error message like below
            if (!File.Exists(dbPath))
            {
                MessageBox.Show($"Database for Lot #{lotNumber} not found in Q:\\Quotes\\FichierDeScie\\Soufflage\\");
                return;
            }

            // Clear previous cut inputs like tbxCutQTY1, tbxCutLength1, etc.
            List<CutItem> loadedCuts = new List<CutItem>();
            _loadedCutsWithDelignage = new List<CutItemWithDelignage>(); // Initialize the delignage list

            // Load data from the database
            try
            {
                string connStr = $@"Provider=Microsoft.Jet.OLEDB.4.0;Data Source={dbPath};Persist Security Info=False;";
                using (OleDbConnection conn = new OleDbConnection(connStr))
                {
                    conn.Open();
                    using (OleDbCommand cmd = new OleDbCommand("SELECT Taille, POS_1 FROM Soufflage ORDER BY IDENTIF, LIGNE", conn))
                    using (OleDbDataReader reader = cmd.ExecuteReader())
                    {
                        while (reader.Read())
                        {
                            if (!reader.IsDBNull(0))
                            {
                                double len = Convert.ToDouble(reader["Taille"]);
                                string delignage = reader.IsDBNull(1) ? "" : reader["POS_1"].ToString();

                                loadedCuts.Add(new CutItem { Quantity = 1, Length = len });
                                _loadedCutsWithDelignage.Add(new CutItemWithDelignage { Length = len, Delignage = delignage });
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

            // Group by delignage for analysis
            var delignageGroups = _loadedCutsWithDelignage.GroupBy(d => d.Delignage)
                .Select(g => new { Delignage = g.Key, Count = g.Count() })
                .OrderByDescending(g => g.Count)
                .ToList();

            // If no delignage values found, show a message and return
            StringBuilder delignageInfo = new StringBuilder();
            delignageInfo.AppendLine("Delignage Values Found:");

            foreach (var group in delignageGroups)
            {
                delignageInfo.AppendLine($"- {group.Delignage}: {group.Count} pieces");
            }

            // Show the delignage information in a message box
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

            // Show the delignage information in a message box
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
        #endregion


        // Method to handle a glitch that was occuring, need this to make sure nothing re-opens once its closed
        private void Form1_FormClosing(object sender, FormClosingEventArgs e)
        {
            Application.Exit(); // Ensure application exits cleanly
        }

        // Method to clear all cut input textboxes when needed
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

        private List<CutItem> ProcessCutsForGroupCutting(List<CutItem> originalCuts, bool isGroupCutting)
        {
            var processedCuts = new List<CutItem>();

            foreach (var cut in originalCuts)
            {
                var processedCut = new CutItem
                {
                    Length = cut.Length,
                    OriginalQuantity = cut.Quantity,
                    IsGroupCut = isGroupCutting
                };

                if (isGroupCutting)
                {
                    // When group cutting, we need fewer actual cuts since each cut produces 2 pieces
                    processedCut.Quantity = (int)Math.Ceiling(cut.Quantity / 2.0);
                }
                else
                {
                    processedCut.Quantity = cut.Quantity;
                }

                processedCuts.Add(processedCut);
            }

            return processedCuts;
        }


        // To clear all textboxes when clicking on the 'CLEAR' button
        private void btnClear_Click(object sender, EventArgs e)
        {
            tbxLotNumber.Clear();
            tbxDeligne.Clear();
            tbxDeligne2.Clear();
            tbxCutLength1.Clear();
            tbxCutLength2.Clear();
            tbxCutLength3.Clear();
            tbxCutLength4.Clear();
            tbxCutLength5.Clear();
            tbxCutLength6.Clear();
            tbxCutLength7.Clear();
            tbxCutLength8.Clear();
            tbxCutLength9.Clear();
            tbxCutLength10.Clear();
            tbxCutLength11.Clear();
            tbxCutLength12.Clear();
            tbxCutLength13.Clear();
            tbxCutLength14.Clear();
            tbxCutQTY1.Clear();
            tbxCutQTY2.Clear();
            tbxCutQTY3.Clear();
            tbxCutQTY4.Clear();
            tbxCutQTY5.Clear();
            tbxCutQTY6.Clear();
            tbxCutQTY7.Clear();
            tbxCutQTY8.Clear();
            tbxCutQTY9.Clear();
            tbxCutQTY10.Clear();
            tbxCutQTY11.Clear();
            tbxCutQTY12.Clear();
            tbxCutQTY13.Clear();
            tbxCutQTY14.Clear();
        }

        private void cbxTwoBoards_CheckedChanged(object sender, EventArgs e)
        {
            CheckBox checkBox = sender as CheckBox;

            if (cbxTwoBoards.Checked)
            {
                string message = "Group Cutting Mode Enabled!\n\n" +
                                 "This is for those who prefer to cut two pieces at once, " +
                                 "This will optimize cuts by grouping them into pairs, " +
                                 "reducing the number of cuts needed. ";

                MessageBox.Show(message, "Group Cutting Information", MessageBoxButtons.OK, MessageBoxIcon.Information);

                UpdateQuantityDisplay(true);
            }
            else
            {
                UpdateQuantityDisplay(false);
            }
        }

        private void UpdateQuantityDisplay(bool groupCuttingEnabled)
        {
            for (int i = 1; i <= 14; i++)
            {
                TextBox qtyBox = (TextBox)this.Controls.Find("tbxCutQTY" + i, true).FirstOrDefault();

                if (qtyBox != null && !string.IsNullOrWhiteSpace(qtyBox.Text))
                {
                    if (groupCuttingEnabled)
                    {
                        qtyBox.BackColor = Color.LightBlue;

                        if (int.TryParse(qtyBox.Text, out int qty))
                        {
                            int groupCuts = (int)Math.Ceiling(qty / 2.0);
                            ToolTip toolTip = new ToolTip();
                            toolTip.SetToolTip(qtyBox, $"Group Cutting: {qty} pieces = {groupCuts} cuts" +
                                              (qty % 2 == 1 ? " (+1 extra piece)" : ""));
                        }
                    }
                    else
                    {
                        qtyBox.BackColor = SystemColors.Window;
                        ToolTip toolTip = new ToolTip();
                        toolTip.SetToolTip(qtyBox, "");
                    }
                }
                else
                {
                    qtyBox.BackColor = SystemColors.Window;
                }
            }
        }

        // Could be used for later on, but for now, not needed (Saved)
        private void ShowGroupCuttingInfo(List<CutItem> originalCuts, List<CutItem> processedCuts)
        {
            StringBuilder info = new StringBuilder();
            info.AppendLine("Group Cutting Enabled - Cutting 2 boards at once:\n");

            for (int i = 0; i < originalCuts.Count; i++)
            {
                var original = originalCuts[i];
                var processed = processedCuts[i];

                info.AppendLine($"Length {original.Length}mm: ");
                info.AppendLine($" - Need: {original.Quantity} pieces");
                info.AppendLine($" - Cuts required: {processed.Quantity} (each cut produces 2 pieces)");

                if (original.Quantity % 2 == 1)
                {
                    info.AppendLine(" - Note: Will produce 1 extra piece due to odd quantity.");
                }
                info.AppendLine();
            }

            int totalOriginalCuts = originalCuts.Sum(c => c.Quantity);
            int totalProcessedCuts = processedCuts.Sum(c => c.Quantity);
            int savedCuts = totalOriginalCuts - totalProcessedCuts;

            info.AppendLine($"Summary:");
            info.AppendLine($" - Original cuts needed: {totalOriginalCuts}");
            info.AppendLine($" - Group cuts needed: {totalProcessedCuts}");
            info.AppendLine($" - Cuts saved: {savedCuts}");

            MessageBox.Show(info.ToString(), "Group Cutting Information", MessageBoxButtons.OK, MessageBoxIcon.Information);
        }

        private void tbxLotNumber_TextChanged(object sender, EventArgs e)
        {
            if (cbxTwoBoards.Checked)
            {
                cbxTwoBoards.Checked = false;
            }
        }
    }
}