using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Data.OleDb;
using System.Data.SqlClient;
using System.Drawing;
using System.Drawing.Printing;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using ThermosProject;

namespace ThermosProject
{
    public partial class frmSecond : Form
    {
        private frmMain mainForm;

        public frmSecond(frmMain mainForm)
        {
            InitializeComponent();
            this.mainForm = mainForm;
        }

        private List<(string Code, string Desc, string Total, string Grill, string Grand)> savedRows
            = new List<(string, string, string, string, string)>();

        private int currentBatch = 1;

        private List<(string Code, string Desc, string Total, string Grill, string Grand)> CaptureCurrentRows()
        {
            var rows = new List<(string, string, string, string, string)>();

            for (int i = 1; i <= 15; i++)
            {
                var code = this.Controls.Find($"tbxCode{i}", true).FirstOrDefault() as TextBox;
                var desc = mainForm.Controls.Find($"tbxDesc{i}", true).FirstOrDefault() as TextBox;
                var total = this.Controls.Find($"tbxTotal{i}", true).FirstOrDefault() as TextBox;
                var grill = this.Controls.Find($"tbxGC{i}", true).FirstOrDefault() as TextBox;
                var grand = this.Controls.Find($"tbxGT{i}", true).FirstOrDefault() as TextBox;

                if (code == null || desc == null || total == null || grill == null || grand == null)
                    continue;

                var c = code.Text?.Trim() ?? "";
                var d = desc.Text?.Trim() ?? "";
                var t = total.Text?.Trim() ?? "";
                var g = grill.Text?.Trim() ?? "";
                var gt = grand.Text?.Trim() ?? "";

                if (!string.IsNullOrEmpty(c) || !string.IsNullOrEmpty(d) || !string.IsNullOrEmpty(t) 
                    || !string.IsNullOrEmpty(g) || !string.IsNullOrEmpty(gt))
                {
                    rows.Add((c, d, t, g, gt));
                }
            }
            return rows;
        }


        private void btnExit_Click(object sender, EventArgs e)
        {
            this.Close();
        }

        private void btnCalculate_Click(object sender, EventArgs e)
        {
            try
            {
                string accessPath = @"Q:\Quotes\Verre\SetupMiOptima.mdb";
                string connString = $"Provider=Microsoft.ACE.OLEDB.12.0;Data Source={accessPath};";

                var priceLookup = LoadPriceDictionary(connString);
                MessageBox.Show($"Loaded {priceLookup.Count} price entries from Access DB");

                double totalSum = 0;
                var debugLines = new List<string>();

                for (int i = 1; i <= 15; i++)
                {
                    TextBox tbxDesc = mainForm.Controls.Find($"tbxDesc{i}", true).FirstOrDefault() as TextBox;
                    TextBox tbxLarg = mainForm.Controls.Find($"tbxLarg{i}", true).FirstOrDefault() as TextBox;
                    TextBox tbxHaut = mainForm.Controls.Find($"tbxHaut{i}", true).FirstOrDefault() as TextBox;
                    TextBox tbxTotal = this.Controls.Find($"tbxTotal{i}", true).FirstOrDefault() as TextBox;

                    if (tbxDesc == null || tbxLarg == null || tbxHaut == null || tbxTotal == null)
                    {
                        debugLines.Add($"Row {i}: controls missing");
                        continue;
                    }

                    string rawDesc = tbxDesc.Text ?? "";
                    string description = rawDesc.Trim(); // don't change case here if you didn't change LoadPriceDictionary

                    if (string.IsNullOrEmpty(description))
                    {
                        tbxTotal.Text = "";
                        debugLines.Add($"Row {i}: empty description -> skipped");
                        continue;
                    }

                    // Try parse larg/haut, tolerant to commas and spaces
                    bool parsedLarg = TryParseDoubleLoose(tbxLarg.Text, out double larg);
                    bool parsedHaut = TryParseDoubleLoose(tbxHaut.Text, out double haut);

                    if (!parsedLarg || !parsedHaut)
                    {
                        tbxTotal.Text = "Err";
                        debugLines.Add($"Row {i}: parse error larg='{tbxLarg.Text}' ({parsedLarg}), haut='{tbxHaut.Text}' ({parsedHaut})");
                        continue;
                    }

                    // Lookup price
                    if (!priceLookup.TryGetValue(description, out double dblPrix))
                    {
                        // try a normalization fallback: trimmed uppercase match (if your dictionary stored uppercase)
                        string alt = description.Trim().ToUpperInvariant();
                        var key = priceLookup.Keys.FirstOrDefault(k => k.ToUpperInvariant() == alt);
                        if (key != null)
                            dblPrix = priceLookup[key];
                    }

                    if (dblPrix <= 0.0)
                    {
                        tbxTotal.Text = "N/A";
                        debugLines.Add($"Row {i}: price not found or zero for '{description}' (dblPrix={dblPrix})");
                        continue;
                    }

                    double total = (larg / 1000.0) * (haut / 1000.0) * dblPrix;
                    tbxTotal.Text = total.ToString("0.00", CultureInfo.InvariantCulture);
                    totalSum += total;

                    debugLines.Add($"Row {i}: desc='{description}', larg={larg}, haut={haut}, price={dblPrix} => total={total:0.00}");
                }

                TextBox tbxTotalSum = this.Controls.Find("tbxTotalSum", true).FirstOrDefault() as TextBox;
                if (tbxTotalSum != null)
                    tbxTotalSum.Text = totalSum.ToString("0.00", CultureInfo.InvariantCulture);

                // Show debug: if it's long show first 2000 chars to avoid giant message boxes
                string debugMsg = string.Join(Environment.NewLine, debugLines);
                if (debugMsg.Length > 3000) debugMsg = debugMsg.Substring(0, 3000) + Environment.NewLine + "...(truncated)";
                MessageBox.Show(debugMsg, "Calculate Debug");
            }
            catch (Exception ex)
            {
                MessageBox.Show("Error calculating totals:\n" + ex.Message);
            }

            // GRILL COST
            try
            {
                var carrelagePrices = LoadCarrelagePrices(@"Q:\Quotes\Verre\Carrelage.mdb");
                var debugLines = new List<string>();
                double grillSum = 0.0;

                for (int i = 1; i <= 15; i++)
                {
                    TextBox tbxCode = mainForm.Controls.Find($"tbxCode{i}", true).FirstOrDefault() as TextBox;
                    TextBox tbxGC = this.Controls.Find($"tbxGC{i}", true).FirstOrDefault() as TextBox;

                    if (tbxCode == null || tbxGC == null)
                        continue;

                    string code = tbxCode.Text.Trim();
                    if (string.IsNullOrEmpty(code))
                    {
                        tbxGC.Text = "";
                        continue;
                    }

                    string strCarrelage = GetStrCarrelageFromSQL(code);
                    if (string.IsNullOrEmpty(strCarrelage))
                    {
                        tbxGC.Text = "N/A";
                        continue;
                    }

                    string[] parts = strCarrelage.Split(';');
                    if (parts.Length < 2)
                    {
                        tbxGC.Text = "Err";
                        debugLines.Add($"Row {i}: Invalid format for '{strCarrelage}'");
                        continue;
                    }

                    string desc = parts[0].Trim();
                    string typeAndMath = parts[1].Trim();

                    int colonIdx = typeAndMath.IndexOf(':');
                    if (colonIdx < 0)
                    {
                        tbxGC.Text = "Err";
                        debugLines.Add($"Row {i}: No ':' found in '{typeAndMath}'");
                        continue;
                    }

                    string type = typeAndMath.Substring(0, colonIdx).Trim();
                    string math = typeAndMath.Substring(colonIdx + 1).Replace(";", "").Trim();

                   var match = System.Text.RegularExpressions.Regex.Match(math, @"(\d+(?:\.\d+)?)\s*[xX]\s*(\d+(?:\.\d+)?)");
                    if (!match.Success)
                    {
                        tbxGC.Text = "Err";
                        debugLines.Add($"Row {i}: Could not parse valid 'NxM' from '{math}'");
                        continue;
                    }

                    double n1 = double.Parse(match.Groups[1].Value, CultureInfo.InvariantCulture);
                    double n2 = double.Parse(match.Groups[2].Value, CultureInfo.InvariantCulture);

                    double baseTotal = n1 * n2;

                    if (type.IndexOf("de tête", StringComparison.OrdinalIgnoreCase) >= 0 ||
                        type.IndexOf("de tete", StringComparison.OrdinalIgnoreCase) >= 0)
                    {
                        baseTotal += 1;
                    }

                    string matchedKey = carrelagePrices.Keys.FirstOrDefault
                        (k => k.IndexOf(desc, StringComparison.OrdinalIgnoreCase) >= 0);
                    if (matchedKey == null)
                    {
                        tbxGC.Text = "N/A";
                        debugLines.Add($"Row {i}: No Carrelage.mdb match for '{desc}'");
                        continue;
                    }

                    double dblPrixS = carrelagePrices[matchedKey];
                    double grillCost = baseTotal * dblPrixS;
                    grillSum += grillCost;

                    tbxGC.Text = grillCost.ToString("0.00", CultureInfo.InvariantCulture);
                    debugLines.Add($"Row {i}: '{desc}' [{type}] => {n1}x{n2}{(baseTotal != n1 * n2 ? " (+1)" : "")}, " +
                       $"{dblPrixS} = {grillCost:0.00}");
                }

                TextBox tbxGCSum = this.Controls.Find("tbxGCSum", true).FirstOrDefault() as TextBox;
                if (tbxGCSum != null)
                    tbxGCSum.Text = grillSum.ToString("0.00", CultureInfo.InvariantCulture);
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Error calculating Grill Costs: {ex.Message}\n\nStackTrace:\n{ex.StackTrace}");
            }

            // GRAND TOTAL 
            try
            {
                double grandSum = 0;

                for (int i = 1; i <= 15; i++)
                {
                    TextBox tbxTotal = this.Controls.Find($"tbxTotal{i}", true).FirstOrDefault() as TextBox;
                    TextBox tbxGC = this.Controls.Find($"tbxGC{i}", true).FirstOrDefault() as TextBox;
                    TextBox tbxGT = this.Controls.Find($"tbxGT{i}", true).FirstOrDefault() as TextBox;

                    if (tbxTotal == null || tbxGC == null || tbxGT == null)
                        continue;

                    double.TryParse(tbxTotal.Text.Replace(',', '.'), NumberStyles.Any, CultureInfo.InvariantCulture, out double glassTotal);
                    double.TryParse(tbxGC.Text.Replace(',', '.'), NumberStyles.Any, CultureInfo.InvariantCulture, out double grillTotal);

                    double rowTotal = glassTotal + grillTotal;
                    tbxGT.Text = rowTotal > 0 ? rowTotal.ToString("0.00", CultureInfo.InvariantCulture) : "";

                    grandSum += rowTotal;
                }

                TextBox tbxGTSum = this.Controls.Find("tbxGTSum", true).FirstOrDefault() as TextBox;
                if (tbxGTSum != null)
                    tbxGTSum.Text = grandSum.ToString("0.00", CultureInfo.InvariantCulture);
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Error calculating Grand Totals: {ex.Message}");
            }
        }

        private Dictionary<string, double> LoadPriceDictionary(string connString)
        {
            var dict = new Dictionary<string, double>(StringComparer.OrdinalIgnoreCase);

            using (OleDbConnection conn = new OleDbConnection(connString))
            {
                conn.Open();

                string query = "SELECT Description, dblPrix FROM Config"; // Change table/field names if needed
                using (OleDbCommand cmd = new OleDbCommand(query, conn))
                using (OleDbDataReader reader = cmd.ExecuteReader())
                {
                    while (reader.Read())
                    {
                        string desc = reader["Description"].ToString().Trim().ToUpper();
                        object prixObj = reader["dblPrix"];
                        double prix = 0;

                        if (prixObj != DBNull.Value)
                            double.TryParse(prixObj.ToString(), out prix);

                        if (!string.IsNullOrEmpty(desc) && !dict.ContainsKey(desc))
                            dict.Add(desc, prix);
                    }
                }
            }

            return dict;
        }


        // Helper: attempt parsing numbers robustly (accepts "1,234.56", "1234,56", " 1234 ")
        private bool TryParseDoubleLoose(string input, out double value)
        {
            value = 0;
            if (string.IsNullOrWhiteSpace(input)) return false;

            input = input.Trim();

            // remove any non numeric trailing/leading characters except decimal separators and minus
            input = input.Replace("\u00A0", " ").Trim();

            // Try Invariant first (dot decimal)
            if (double.TryParse(input, NumberStyles.AllowDecimalPoint | NumberStyles.AllowThousands | NumberStyles.AllowLeadingSign, CultureInfo.InvariantCulture, out value))
                return true;

            // Try current culture (to allow comma decimal)
            if (double.TryParse(input, NumberStyles.AllowDecimalPoint | NumberStyles.AllowThousands | NumberStyles.AllowLeadingSign, CultureInfo.CurrentCulture, out value))
                return true;

            // As a final fallback, replace comma with dot and try invariant
            var replaced = input.Replace(",", ".");
            if (double.TryParse(replaced, NumberStyles.AllowDecimalPoint | NumberStyles.AllowThousands | NumberStyles.AllowLeadingSign, CultureInfo.InvariantCulture, out value))
                return true;

            return false;
        }

        // Another helper: 
        private Dictionary<string, double> LoadCarrelagePrices(string path)
        {
            var dict = new Dictionary<string, double>(StringComparer.OrdinalIgnoreCase);

            using (OleDbConnection conn = new OleDbConnection(
                $"Provider=Microsoft.ACE.OLEDB.12.0;Data Source={path}"))
            {
                conn.Open();
                string query = "SELECT strCarrelage, dblPrixS FROM Liste";
                using (OleDbCommand cmd = new OleDbCommand(query, conn))
                using (OleDbDataReader reader = cmd.ExecuteReader())
                {
                    while (reader.Read())
                    {
                        string desc = reader["strCarrelage"].ToString().Trim();
                        if (!double.TryParse(reader["dblPrixS"].ToString(), out double prix)) prix = 0;
                        if (!string.IsNullOrEmpty(desc) && !dict.ContainsKey(desc))
                            dict.Add(desc, prix);
                    }
                }
            }
            return dict;
        }

        private string GetStrCarrelageFromSQL(string code)
        {
            string result = null;

            string connStr = "Data Source=10.0.7.2;Initial Catalog=Verres_Dalumex;User ID=SuiviProd;Password=SuiviProd;";

            using (SqlConnection conn = new SqlConnection(connStr))
            {
                conn.Open();
                string query = "SELECT strCarrelage FROM dbo.viewVerres WHERE strCodeBarre = @code";
                using (SqlCommand cmd = new SqlCommand(query, conn))
                {
                    cmd.Parameters.AddWithValue("@code", code);
                    var val = cmd.ExecuteScalar();
                    if (val != null && val != DBNull.Value)
                        result = val.ToString();
                }
            }
            return result;
        }

        private void frmSecond_Load(object sender, EventArgs e)
        {
            savedRows.Clear();
            currentBatch = 1;

            for (int i = 1; i <= 15; i++)
            {
                TextBox mainTbx = mainForm.Controls.Find($"tbxCode{i}", true).FirstOrDefault() as TextBox;
                TextBox secondTbx = this.Controls.Find($"tbxCode{i}", true).FirstOrDefault() as TextBox;

                if (mainTbx != null && secondTbx != null)
                    secondTbx.Text = mainTbx.Text;
            }
        }

        private void btnPrint_Click(object sender, EventArgs e)
        {
            try
            {
                var current = CaptureCurrentRows();
                foreach (var row in current)
                {
                    if (!savedRows.Any(r => r.Code == row.Code && r.Desc == row.Desc &&
                        r.Total == row.Total && r.Grill == row.Grill && r.Grand == row.Grand))
                    {
                        savedRows.Add(row);
                    }
                }

                const int MaxPrintableRows = 25;
                if (savedRows.Count > MaxPrintableRows)
                {
                    savedRows = savedRows.Take(MaxPrintableRows).ToList();
                }

                    PrintDocument printDoc = new PrintDocument();

                // FIX: Use the constructor directly, not PrintPageEventHandler()
                printDoc.PrintPage += new PrintPageEventHandler(PrintDoc_PrintPage);

                printDoc.DefaultPageSettings.Landscape = true;

                PrintPreviewDialog previewDialog = new PrintPreviewDialog();
                previewDialog.Document = printDoc;
                previewDialog.Width = 1200;
                previewDialog.Height = 800;
                previewDialog.ShowDialog();
            }
            catch (Exception ex)
            {
                MessageBox.Show("Error during printing:\n" + ex.Message);
            }
        }

        private void PrintDoc_PrintPage(object sender, PrintPageEventArgs e)
        {
            // Fonts and layout setup
            Font titleFont = new Font("Arial", 18, FontStyle.Bold);
            Font headerFont = new Font("Arial", 12, FontStyle.Bold);
            Font subHeaderFont = new Font("Arial", 9, FontStyle.Italic);
            Font textFont = new Font("Arial", 10);
            Brush brush = Brushes.Black;

            float y = 80; // top margin
            float leftMargin = 60;
            float colCode = leftMargin;
            float colDesc = leftMargin + 170;
            float colGlass = leftMargin + 680;
            float colGrill = leftMargin + 795;
            float colGrand = leftMargin + 900;
            float rowHeight = 25;

            // Appears top left of the horizontal report
            string logoPath = @"C:\Users\alexis\source\repos\dalmen\ThermosProject\Resources\Logo-Dalmen (1).png";
            if (System.IO.File.Exists(logoPath))
            {
                Image logo = Image.FromFile(logoPath);
                e.Graphics.DrawImage(logo, leftMargin, 20, 100, 40);
            }

            // Title
            e.Graphics.DrawString("Total Cost Breakdown", titleFont, brush, leftMargin + 200, 20);

            // Headers
            e.Graphics.DrawString("Codes", headerFont, brush, colCode, y);
            e.Graphics.DrawString("Descriptions", headerFont, brush, colDesc, y);
            e.Graphics.DrawString("Glass Total", headerFont, brush, colGlass, y);
            e.Graphics.DrawString("Grill Cost", headerFont, brush, colGrill, y);
            e.Graphics.DrawString("Grand Total", headerFont, brush, colGrand, y);
            y += 20;
            e.Graphics.DrawString("Code Barres", subHeaderFont, brush, colCode, y);
            e.Graphics.DrawString("Descriptions", subHeaderFont, brush, colDesc, y);
            e.Graphics.DrawString("Verres", subHeaderFont, brush, colGlass, y);
            e.Graphics.DrawString("Carrelage", subHeaderFont, brush, colGrill, y);
            e.Graphics.DrawString("Totale Complet", subHeaderFont, brush, colGrand, y);
            y += 25;

            // Horizontal line under headers
            e.Graphics.DrawLine(Pens.Black, leftMargin, y, colGrand + 120, y);
            y += 10;

            var rowsToPrint = savedRows.Take(25).ToList();
            double grandTotalSum = 0;

            // Loop through rows 1–15
            foreach (var row in rowsToPrint)
            {

                string code = row.Code;
                string desc = row.Desc;
                string glass = row.Total;
                string grill = row.Grill;
                string grand = row.Grand;

                // Skip empty rows
                if (string.IsNullOrEmpty(code) && string.IsNullOrEmpty(desc))
                    continue;

                // Draw text for each column
                e.Graphics.DrawString(code, textFont, brush, colCode, y);
                e.Graphics.DrawString(desc, textFont, brush, colDesc, y);
                e.Graphics.DrawString(glass, textFont, brush, colGlass, y);
                e.Graphics.DrawString(grill, textFont, brush, colGrill, y);
                e.Graphics.DrawString(grand, textFont, brush, colGrand, y);


                // Try add to grand total
                if (double.TryParse(grand.Replace(',','.'), System.Globalization.NumberStyles.Any, 
                    System.Globalization.CultureInfo.InvariantCulture, out double gt))
                    grandTotalSum += gt;

                y += rowHeight; // next row
            }

            // Draw final horizontal line
            e.Graphics.DrawLine(Pens.Black, leftMargin, y, colGrand + 120, y);
            y += 10;

            // Print final total sum
            float totalLabelX = colGrill - 40;          // position for the label
            float totalValueX = colGrand;     // push the total amount further right (add spacing)
            float totalY = y + 5;                  // slight vertical adjust if needed

            e.Graphics.DrawString("Overall Total:", headerFont, brush, totalLabelX, totalY);
            e.Graphics.DrawString(grandTotalSum.ToString("C2"), headerFont, brush, totalValueX, totalY);
        }

        private void btnSaveBatch_Click(object sender, EventArgs e)
        {
            if (currentBatch == 1 && savedRows.Count >= 15)
            {
                savedRows.Clear();
            }

            for (int i = 1; i <= 15; i++)
            {
                var code = this.Controls.Find($"tbxCode{i}", true).FirstOrDefault() as TextBox;
                var total = this.Controls.Find($"tbxTotal{i}", true).FirstOrDefault() as TextBox;
                var grill = this.Controls.Find($"tbxGC{i}", true).FirstOrDefault() as TextBox;
                var grand = this.Controls.Find($"tbxGT{i}", true).FirstOrDefault() as TextBox;
                var desc = mainForm.Controls.Find($"tbxDesc{i}", true).FirstOrDefault() as TextBox;

                if (code == null || desc == null || total == null || grill == null || grand == null)
                    continue;

                if (!string.IsNullOrWhiteSpace(code.Text) || !string.IsNullOrWhiteSpace(desc.Text))
                {
                    savedRows.Add((code.Text, desc.Text, total.Text, grill.Text, grand.Text));
                }

                code.Clear();
                total.Clear();
                grill.Clear();
                grand.Clear();
            }

            MessageBox.Show("Batch saved. You can now load in your second batch of 15.", "SAVED", MessageBoxButtons.OK);

            if (currentBatch == 1)
            {
                for (int i = 11; i <= 15; i++)
                {
                    var code = this.Controls.Find($"tbxCode{i}", true).FirstOrDefault() as TextBox;
                    var total = this.Controls.Find($"tbxTotal{i}", true).FirstOrDefault() as TextBox;
                    var grill = this.Controls.Find($"tbxGC{i}", true).FirstOrDefault() as TextBox;
                    var grand = this.Controls.Find($"tbxGT{i}", true).FirstOrDefault() as TextBox;

                    if (code != null) code.Visible = false;
                    if (total != null) total.Visible = false;
                    if (grill != null) grill.Visible = false;
                    if (grand != null) grand.Visible = false;

                }

                MessageBox.Show("Switched to the second batch. (10 entries only).");
                currentBatch = 2;
            }
            else
            {
                MessageBox.Show("All batches saved. You can now print the results.", "ALL SAVED", MessageBoxButtons.OK);
            }
        }
    }
}

