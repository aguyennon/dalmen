using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Data.SqlClient;
using System.Drawing;
using System.Drawing.Printing;
using System.Linq;
using System.Linq.Expressions;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using ZXing;

namespace BarcodeGenerator
{
    public partial class frmDB : Form
    {
        private PrintDocument printDoc;
        private Bitmap memoryImagel;

        private List<BarcodeData> barcodeQueue = new List<BarcodeData>();

        // Getters and setters for barcode data.
        private class BarcodeData
        {
            public string Code { get; set; }
            public string Description { get; set; }
            public Image Image { get; set; }
        }
        public frmDB()
        {
            InitializeComponent();
        }

        private void btnBack_Click(object sender, EventArgs e)
        {
            // Close so it just sends you back to the main form
            this.Close();
        }

        private void btnExit_Click(object sender, EventArgs e)
        {
            // Application exit to shut the entire system
            Application.Exit();
        }

        // Clears.
        private void btnClear_Click(object sender, EventArgs e)
        {
            tbxBarcode.Text = "";
            pbxBarcode.Image = null;
            lblDescInfo.Text = null;
        }

        /// <summary>
        /// Typical print button (regular use) to print the singular barcode and description onto sticker paper.
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void btnPrint_Click(object sender, EventArgs e)
        {
            PrintDocument printDoc = new PrintDocument();
            printDoc.PrintPage += PrintDoc_PrintPage;

            PrintDialog printDialog = new PrintDialog();
            printDialog.Document = printDoc;

            if (printDialog.ShowDialog() == DialogResult.OK)
            {
                printDoc.Print();

                if (!string.IsNullOrEmpty(tbxBarcode.Text))
                {
                    UpdateRecordHistory(tbxBarcode.Text);
                }
            }

            SaveToPDF();
        }

        /// <summary>
        /// Helper method to format the print page for a single barcode.
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void PrintDoc_PrintPage(object sender, PrintPageEventArgs e)
        {
            int yOffset = e.MarginBounds.Top;
            int verticalSpacing = 100;
            int horizontalSpacing = 330;
            int bOffset = e.MarginBounds.Bottom;

            if (pbxBarcode.Image != null)
            {
                Bitmap bmp1 = new Bitmap(pbxBarcode.Width, pbxBarcode.Height);
                pbxBarcode.DrawToBitmap(bmp1, new Rectangle(0, 0, pbxBarcode.Width, pbxBarcode.Height));
                e.Graphics.DrawImage(bmp1, e.MarginBounds.Left, yOffset);

                // Add the code below first barcode
                if (!string.IsNullOrEmpty(tbxBarcode.Text))
                {
                    using (Font font = new Font("Arial", 12, FontStyle.Bold))
                    {
                        SizeF textSize = e.Graphics.MeasureString(tbxBarcode.Text, font);
                        float textX = e.MarginBounds.Left + (bmp1.Width - textSize.Width) / 2;
                        float textY = yOffset + bmp1.Height + 10; // Increased gap

                        // Draw a background rectangle to make sure text is visible
                        e.Graphics.FillRectangle(Brushes.White, textX - 2, textY - 2, textSize.Width + 4, textSize.Height + 4);
                        e.Graphics.DrawString(tbxBarcode.Text, font, Brushes.Black, textX, textY);
                    }
                }

                if (!string.IsNullOrEmpty(lblDescInfo.Text))
                {
                    using (Font descFont = new Font("Arial", 12, FontStyle.Regular))
                    {
                        SizeF descSize = e.Graphics.MeasureString(lblDescInfo.Text, descFont);
                        float descX = e.MarginBounds.Left + (bmp1.Width - descSize.Width) / 2;
                        float descY = yOffset + bmp1.Height + 40;

                        e.Graphics.FillRectangle(Brushes.White, descX - 2, descY - 2, descSize.Width + 4, descSize.Height + 4);
                        e.Graphics.DrawString(lblDescInfo.Text, descFont, Brushes.Black, descX, descY);
                    }
                }

                bmp1.Dispose();
            }

            yOffset += verticalSpacing;
            int xOffset = e.MarginBounds.Left - 130;
        }

        // Helper method to save the barcode pages .
        private void SaveToPDF()
        {
            if (pbxBarcode.Image != null && lblDescInfo.Text != null)
            {
                SaveFileDialog saveDialog = new SaveFileDialog();
                saveDialog.Filter = "PNG files (*.png)|*.png";
                saveDialog.DefaultExt = "png";
                saveDialog.FileName = $"barcode_{tbxBarcode.Text}";

                if (saveDialog.ShowDialog() == DialogResult.OK)
                {

                    try
                    {
                        string extension = System.IO.Path.GetExtension(saveDialog.FileName).ToLower();
                        System.Drawing.Imaging.ImageFormat format = System.Drawing.Imaging.ImageFormat.Png;

                        switch (extension)
                        {
                            case ".jpg":
                            case ".jpeg":
                                format = System.Drawing.Imaging.ImageFormat.Jpeg;
                                break;
                            case ".bmp":
                                format = System.Drawing.Imaging.ImageFormat.Bmp;
                                break;
                            default:
                                format = System.Drawing.Imaging.ImageFormat.Png;
                                break;
                        }

                        pbxBarcode.Image.Save(saveDialog.FileName, format);
                        MessageBox.Show("Barcode saved successfully.");
                    }
                    catch (Exception ex)
                    {
                        MessageBox.Show("Error saving barcode: " + ex.Message);
                    }
                }
            }
            else
            {
                MessageBox.Show("Please generate a barcode first.");
            }
        }

        /// <summary>
        /// This button's click event fetches the description (if any) linked from the database for the entered code.
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void btnFetchDesc_Click(object sender, EventArgs e)
        {
            string barcode = tbxBarcode.Text.Trim();

            if (string.IsNullOrEmpty(barcode))
            {
                MessageBox.Show("Please enter a barcode beforehand.");
                return;
            }

            string connectionString = "Data Source=10.0.7.2;Initial Catalog=BDInventaire;User ID=SuiviProd;Password=SuiviProd;";
            string query = "SELECT invDESCRIPTION FROM dbo.tblInventaire WHERE invCODE = @code";

            try
            {
                using (SqlConnection conn = new SqlConnection(connectionString))
                using (SqlCommand cmd = new SqlCommand(query, conn))
                {
                    cmd.Parameters.AddWithValue("@code", barcode);

                    conn.Open();
                    object result = cmd.ExecuteScalar();
                    conn.Close();

                    if (result != null && result != DBNull.Value)
                    {
                        string description = result.ToString();
                        lblDescInfo.Text = description;
                    }
                    else
                    {
                        lblDescInfo.Text = "No description found for this barcode.";
                    }
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show("Error connecting to database:\n" + ex.Message);
            }

        }

        /// <summary>
        /// This button's click event simply generates a barcode from the entered code.
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void btnGenCode_Click(object sender, EventArgs e)
        {
            string barcodeText = "";
            PictureBox targetPictureBox = null;

            if (!string.IsNullOrEmpty(tbxBarcode.Text))
            {
                barcodeText = tbxBarcode.Text;
                targetPictureBox = pbxBarcode;
            }

            if (string.IsNullOrEmpty(barcodeText))
            {
                MessageBox.Show("Please enter a barcode before trying to generate it.");
                return;
            }

            try
            {
                BarcodeWriter writer = new BarcodeWriter();
                writer.Format = BarcodeFormat.CODE_128;

                int barcodeWidth = Math.Max(700, barcodeText.Length * 50);

                writer.Options = new ZXing.Common.EncodingOptions
                {
                    Height = 50,
                    Width = 500,
                    Margin = 20,
                    PureBarcode = true,
                };

                Bitmap barcodeBitmap = writer.Write(barcodeText);
                targetPictureBox.Image = barcodeBitmap;
            }
            catch (Exception ex)
            {
                MessageBox.Show("Error generating the barcode: " + ex.Message);
            }
        }

        /// <summary>
        /// This button's click event saves up to 7 barcodes and stores them ready for printing.
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void btnSaveForLayout_Click(object sender, EventArgs e)
        {

            if (tbxBarcode == null)
            {
                MessageBox.Show("Please generate a barcode beforehand.");
                return;
            }


            BarcodeData data = new BarcodeData();

            if (tbxBarcode != null)
            {
                data.Code = tbxBarcode.Text;
                data.Image = new Bitmap(pbxBarcode.Image);
                data.Description = lblDescInfo.Text ?? ""; 
            }

            barcodeQueue.Add(data);

            UpdateRecordHistory(data.Code);

            MessageBox.Show($"Barcode has been saved! ({barcodeQueue.Count}/7)");

            tbxBarcode.Text = "";
            pbxBarcode.Image = null;
            lblDescInfo.Text = null;

        }

        /// <summary>
        /// This button's click event takes the stored barcodes from 'Save for Layout' and prints them from the formatted layout.
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void btnPrintPaper_Click(object sender, EventArgs e)
        {
            if (barcodeQueue.Count == 0)
            {
                MessageBox.Show("No barcodes in queue. Please add barcodes using 'Save for Layout' button.");
                return;
            }

            PrintDocument printDoc = new PrintDocument();
            printDoc.PrintPage += PrintBatchPage;

            PrintDialog printDialog = new PrintDialog();
            printDialog.Document = printDoc;

            if (printDialog.ShowDialog() == DialogResult.OK)
            {
                printDoc.Print();
            }
        }

        // Print button's helper method to format the batch page
        private void PrintBatchPage(object sender, PrintPageEventArgs e)
        {
            int yOffset = e.MarginBounds.Top;
            int spacing = 25;

            string lastBarcodeCode = "";

            for (int i = 0; i < barcodeQueue.Count && i < 7; i++)
            {
                BarcodeData data = barcodeQueue[i];

                lastBarcodeCode = data.Code;

                e.Graphics.DrawImage(data.Image, e.MarginBounds.Left, yOffset);

                // Calculate actual image dimensions for text positioning
                int imageHeight = data.Image.Height;
                int imageWidth = data.Image.Width;

                // Draw code text
                using (Font codeFont = new Font("Arial", 12, FontStyle.Regular))
                {
                    SizeF codeSize = e.Graphics.MeasureString(data.Code, codeFont);
                    float codeX = e.MarginBounds.Left + (imageWidth - codeSize.Width) / 2;
                    float codeY = yOffset + imageHeight + 5;
                    e.Graphics.DrawString(data.Code, codeFont, Brushes.Black, codeX, codeY);
                }

                // Draw description text
                if (!string.IsNullOrEmpty(data.Description))
                {
                    using (Font descFont = new Font("Arial", 12, FontStyle.Bold))
                    {
                        SizeF descSize = e.Graphics.MeasureString(data.Description, descFont);
                        float descX = e.MarginBounds.Left + (imageWidth - descSize.Width) / 2;
                        float descY = yOffset + imageHeight + 25;
                        e.Graphics.DrawString(data.Description, descFont, Brushes.Black, descX, descY);
                    }
                }

                float lineY = yOffset + imageHeight + 50;
                e.Graphics.DrawLine(Pens.Gray, e.MarginBounds.Left, lineY, e.MarginBounds.Right, lineY);

                yOffset += imageHeight + 60 + spacing;
            }

            if (!string.IsNullOrEmpty(lastBarcodeCode))
            {
                UpdateRecordHistory(lastBarcodeCode);
            }

            foreach (var data in barcodeQueue)
            {
                data.Image?.Dispose();
            }
            barcodeQueue.Clear();

            MessageBox.Show("Batch print completed! Click OK to confirm and proceed to printing.");
        }

        /// <summary>
        /// This button's click event saves the barcodes (once they're stacked up to 7) into a "pdf" file. (png for now)
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void btnPDFSaved_Click(object sender, EventArgs e)
        {
            if (barcodeQueue.Count == 0)
            {
                MessageBox.Show("No barcodes in queue. Please add barcodes using 'Save for Layout' button.");
                return;
            }

            SaveFileDialog saveDialog = new SaveFileDialog();
            saveDialog.Filter = "PDF files (*.pdf)|*.pdf";
            saveDialog.DefaultExt = "pdf";
            saveDialog.FileName = $"barcode_batch_{DateTime.Now:yyyyMMdd_HHmmss}";

            if (saveDialog.ShowDialog() == DialogResult.OK)
            {
                try
                {
                    int pageWidth = 850;
                    int pageHeight = 1100;
                    string lastBarcodeCode = "";

                    using (Bitmap bmp = new Bitmap(pageWidth, pageHeight))
                    using (Graphics g = Graphics.FromImage(bmp))
                    {
                        g.Clear(Color.White);

                        int yOffset = 50; // Top margin
                        int spacing = 25;
                        int leftMargin = 50;

                        for (int i = 0; i < barcodeQueue.Count && i < 7; i++)
                        {
                            BarcodeData data = barcodeQueue[i];

                            lastBarcodeCode = data.Code;

                            // Draw barcode image
                            g.DrawImage(data.Image, leftMargin, yOffset);

                            int imageHeight = data.Image.Height;
                            int imageWidth = data.Image.Width;

                            // Draw code text
                            using (Font codeFont = new Font("Arial", 12, FontStyle.Regular))
                            {
                                SizeF codeSize = g.MeasureString(data.Code, codeFont);
                                float codeX = leftMargin + (imageWidth - codeSize.Width) / 2;
                                float codeY = yOffset + imageHeight + 5;
                                g.DrawString(data.Code, codeFont, Brushes.Black, codeX, codeY);
                            }

                            // Draw description text
                            if (!string.IsNullOrEmpty(data.Description))
                            {
                                using (Font descFont = new Font("Arial", 12, FontStyle.Bold))
                                {
                                    SizeF descSize = g.MeasureString(data.Description, descFont);
                                    float descX = leftMargin + (imageWidth - descSize.Width) / 2;
                                    float descY = yOffset + imageHeight + 25;
                                    g.DrawString(data.Description, descFont, Brushes.Black, descX, descY);
                                }
                            }

                            // Separator line
                            float lineY = yOffset + imageHeight + 50;
                            g.DrawLine(Pens.Gray, leftMargin, lineY, leftMargin + imageWidth, lineY);

                            yOffset += imageHeight + 60 + spacing;
                        }

                        // Save as PNG instead (direct PDF requires additional libraries)
                        bmp.Save(saveDialog.FileName.Replace(".pdf", ".png"), System.Drawing.Imaging.ImageFormat.Png);
                    }

                    if (!string.IsNullOrEmpty(lastBarcodeCode))
                    {
                        UpdateRecordHistory(lastBarcodeCode);
                    }

                    MessageBox.Show("Batch saved successfully as PNG!\n\nNote: To save as actual PDF, you'll need to install a PDF library like iTextSharp or PdfSharp.");
                }
                catch (Exception ex)
                {
                    MessageBox.Show("Error saving batch: " + ex.Message);
                }
            }
        }

        private void frmDB_Load(object sender, EventArgs e)
        {

        }

        private void lblRecordHistory_Click(object sender, EventArgs e)
        {

        }

        private void UpdateRecordHistory(string barcodeCode)
        {
            lblRecordHistory.Text = $"Last Recorded Saved Barcode: {barcodeCode}";
        }
    }
}
