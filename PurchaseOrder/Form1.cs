using iTextSharp.text.pdf;
using iTextSharp.text;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Drawing.Imaging;
using System.Drawing.Printing;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using Color = System.Drawing.Color;
using Font = iTextSharp.text.Font;

namespace PurchaseOrder
{
    public partial class Form1 : Form
    {
        private int currentPONumber;
        private string settingsFile = "POSettings.txt";
        private PrintDocument printDocument = new PrintDocument();
        private Bitmap memoryImage;
        public Form1()
        {
            InitializeComponent();
            
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            LoadPONumber();
            tbxPO.Text = currentPONumber.ToString();
            printDocument.PrintPage += PrintDocument_PrintPage;
        }

        private void LoadPONumber()
        {
            try
            {
                if (File.Exists(settingsFile))
                {
                    string poText = File.ReadAllText(settingsFile);
                    if (int.TryParse(poText, out int po))
                    {
                        currentPONumber = po;
                    }
                    else
                    {
                        currentPONumber = 1000;
                    }
                }
                else
                {
                    currentPONumber = 1000;
                }
            }
            catch
            {
                currentPONumber = 1000;
            }
        }

        private void SavePONumber()
        {
            try
            {
                File.WriteAllText(settingsFile, currentPONumber.ToString());
            }
            catch
            {
                MessageBox.Show("Error saving page.");
            }
        }

        private void IncrementPONumber()
        {
            currentPONumber++;
            tbxPO.Text = currentPONumber.ToString();
            SavePONumber();
        }

        private void btnPrintPDF_Click(object sender, EventArgs e)
        {
            SaveAsFillablePDF();
            PrintForm();
            IncrementPONumber();
            ClearForm();
        }

        private void CaptureScreen()
        {
            Size clientSize = this.ClientSize;

            int excludedHeight = Math.Max(btnPrintPDF.Height, btnExit.Height);
            int captureHeight = clientSize.Height - excludedHeight - 15;

            // Create bitmap for the client area only
            memoryImage = new Bitmap(clientSize.Width, clientSize.Height);
            Graphics memoryGraphics = Graphics.FromImage(memoryImage);

            // Fill with white background (or make transparent)
            memoryGraphics.Clear(Color.White); // Use Color.Transparent for transparent background

            // Calculate the position of the client area on screen
            Point clientLocation = this.PointToScreen(Point.Empty);

            // Capture only the client area (no title bar, no borders)
            memoryGraphics.CopyFromScreen(
                clientLocation.X,
                clientLocation.Y,
                0,
                0,

                new Size(clientSize.Width, captureHeight));


        }

        private void PrintForm()
        {
            CaptureScreen();
            printDocument.Print();
        }

        private void PrintDocument_PrintPage(object sender, PrintPageEventArgs e)
        {
            e.Graphics.DrawImage(memoryImage, 0, 0);
        }

        private void SaveAsFillablePDF()
        {
            string folderPath = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.MyDocuments), "PurchaseOrders");

            Directory.CreateDirectory(folderPath);
            string filePath = Path.Combine(folderPath, $"PO_{currentPONumber}_{DateTime.Now:yyyyMMdd}.pdf");

            using (FileStream fs = new FileStream(filePath, FileMode.Create, FileAccess.Write))
            {
                Document doc = new Document(PageSize.A4, 50, 50, 50, 50);
                PdfWriter writer = PdfWriter.GetInstance(doc, fs);
                doc.Open();

                PdfContentByte cb = writer.DirectContent;

                // LOGO
                if (pbxLogo.Image != null)
                {
                    using (MemoryStream ms = new MemoryStream())
                    {
                        pbxLogo.Image.Save(ms, System.Drawing.Imaging.ImageFormat.Png);
                        ms.Position = 0;

                        iTextSharp.text.Image logo = iTextSharp.text.Image.GetInstance(ms);
                        logo.ScaleAbsolute(200f, 100f);
                        logo.SetAbsolutePosition(60f, 730f);
                        doc.Add(logo);
                    }
                }

                cb.BeginText();
                cb.SetFontAndSize(BaseFont.CreateFont(), 12);
                cb.ShowTextAligned(PdfContentByte.ALIGN_LEFT, "5630 St-Catherine", 60, 690, 0);
                cb.ShowTextAligned(PdfContentByte.ALIGN_LEFT, "St-Isidore, Ontario", 60, 678, 0);
                cb.ShowTextAligned(PdfContentByte.ALIGN_LEFT, "K0C 2B0", 60, 666, 0);
                cb.ShowTextAligned(PdfContentByte.ALIGN_LEFT, "(613) 524-2268", 60, 654, 0);
                cb.EndText();

                // BOX TOP RIGHT
                float boxX = 350f;
                float boxY = 640f;
                float boxWidth = 230f;
                float boxHeight = 180f;

                cb.Rectangle(boxX, boxY, boxWidth, boxHeight);
                cb.Stroke();

                // Title centered in box
                float boxCenterX = boxX + (boxWidth / 2);
                float titleY = boxY + boxHeight - 20f; // 20px from top of box

                ColumnText.ShowTextAligned(cb, Element.ALIGN_CENTER,
                    new Phrase("Purchase Order", FontFactory.GetFont(FontFactory.HELVETICA_BOLD, 14)),
                    boxCenterX, titleY, 0);

                // Field setup
                float leftX = boxX + 10f;  // 10px padding from left edge of box
                float fieldWidth = 90f;
                float fieldHeight = 18f;
                float labelWidth = 100f;
                float rowGap = 30f;
                float startY = boxY + boxHeight - 50f; // Start below title

                float y = startY;

                // DATE
                float fieldX = boxX + boxWidth - fieldWidth - 10f; // Right-aligned with padding
                cb.Rectangle(fieldX, y, fieldWidth, fieldHeight);
                cb.Stroke();
                ColumnText.ShowTextAligned(cb, Element.ALIGN_LEFT, new Phrase("Date:"), leftX, y + 3, 0);
                TextField dateField = new TextField(writer, new iTextSharp.text.Rectangle(fieldX, y, fieldX + fieldWidth, y + fieldHeight), "Date");
                dateField.Text = DateTime.Now.ToString("dd MMM yyyy");
                writer.AddAnnotation(dateField.GetTextField());
                y -= rowGap;

                // PO NUMBER
                cb.Rectangle(fieldX, y, fieldWidth, fieldHeight);
                cb.Stroke();
                ColumnText.ShowTextAligned(cb, Element.ALIGN_LEFT, new Phrase("P.O. #:"), leftX, y + 3, 0);
                TextField poField = new TextField(writer, new iTextSharp.text.Rectangle(fieldX, y, fieldX + fieldWidth, y + fieldHeight), "PO");
                poField.Text = currentPONumber.ToString();
                writer.AddAnnotation(poField.GetTextField());
                y -= rowGap;

                // NAME
                cb.Rectangle(fieldX, y, fieldWidth, fieldHeight);
                cb.Stroke();
                ColumnText.ShowTextAligned(cb, Element.ALIGN_LEFT, new Phrase("Name:"), leftX, y + 3, 0);
                TextField nameField = new TextField(writer, new iTextSharp.text.Rectangle(fieldX, y, fieldX + fieldWidth, y + fieldHeight), "Name");
                nameField.Text = tbxName.Text;
                writer.AddAnnotation(nameField.GetTextField());
                y -= rowGap;

                // SUPPLIER
                cb.Rectangle(fieldX, y, fieldWidth, fieldHeight);
                cb.Stroke();
                ColumnText.ShowTextAligned(cb, Element.ALIGN_LEFT, new Phrase("Supplier:"), leftX, y + 3, 0);
                TextField supplierField = new TextField(writer, new iTextSharp.text.Rectangle(fieldX, y, fieldX + fieldWidth, y + fieldHeight), "Supplier");
                supplierField.Text = tbxSupplierName.Text;
                writer.AddAnnotation(supplierField.GetTextField());
                y -= rowGap;

                // COMMANDE
                cb.Rectangle(fieldX, y, fieldWidth, fieldHeight);
                cb.Stroke();
                ColumnText.ShowTextAligned(cb, Element.ALIGN_LEFT, new Phrase("# de Commande:"), leftX, y + 3, 0);
                TextField commandeField = new TextField(writer, new iTextSharp.text.Rectangle(fieldX, y, fieldX + fieldWidth, y + fieldHeight), "Commande");
                commandeField.Text = tbxCommande.Text;
                writer.AddAnnotation(commandeField.GetTextField());

                // For each section in header
                float tableTopY = 550f;
                float xQty = 60f;
                float xDesc = 150f; 
                float xUom = 500f;
                float rowHeight = 25f;

                // HEADER
                BaseFont bfBold = BaseFont.CreateFont(BaseFont.HELVETICA_BOLD, BaseFont.CP1252, false);
                cb.BeginText();
                cb.SetFontAndSize(bfBold, 11);
                cb.ShowTextAligned(PdfContentByte.ALIGN_LEFT, "QTY", xQty, tableTopY + 10, 0);
                cb.ShowTextAligned(PdfContentByte.ALIGN_LEFT, "Description", xDesc, tableTopY + 10, 0);
                cb.ShowTextAligned(PdfContentByte.ALIGN_LEFT, "Unit of Measure", xUom, tableTopY + 10, 0);
                cb.EndText();

                for (int i = 1; i <= 8; i++)
                {
                    float yPosition = tableTopY - (i * rowHeight);

                    // qty
                    cb.Rectangle(xQty, yPosition, 60f, 18f);
                    cb.Stroke();
                    TextField qtyField = new TextField(writer, new iTextSharp.text.Rectangle(xQty, yPosition, xQty + 60, yPosition + 18), $"qty{i}");
                    qtyField.Text = GetTextBoxValue($"tbxQty{i}");
                    writer.AddAnnotation(qtyField.GetTextField());

                    cb.Rectangle(xDesc, yPosition, 320f, 18f);
                    cb.Stroke();
                    TextField descField = new TextField(writer, new iTextSharp.text.Rectangle(xDesc, yPosition, xDesc + 320, yPosition + 18), $"desc{i}");
                    descField.Text = GetTextBoxValue($"tbxDesc{i}");
                    writer.AddAnnotation(descField.GetTextField());

                    cb.Rectangle(xUom, yPosition, 60f, 18f);
                    cb.Stroke();
                    TextField uomField = new TextField(writer, new iTextSharp.text.Rectangle(xUom, yPosition, xUom + 60, yPosition + 18), $"uom{i}");
                    uomField.Text = GetTextBoxValue($"tbxUOM{i}");
                    writer.AddAnnotation(uomField.GetTextField());
                }

                // COLOUR SELECTION
                cb.BeginText();
                cb.SetFontAndSize(BaseFont.CreateFont(), 11);
                cb.ShowTextAligned(PdfContentByte.ALIGN_LEFT, "Exterior Color:", 60, 120, 0);
                cb.ShowTextAligned(PdfContentByte.ALIGN_LEFT, "Interior Color:", 320, 120, 0);
                cb.EndText();

                cb.Rectangle(60f, 100f, 240f, 18f);
                cb.Stroke();
                TextField colorExt = new TextField(writer, new iTextSharp.text.Rectangle(60, 100, 300, 118), "ExteriorColor");
                colorExt.Text = cbxExtCol.Text;
                writer.AddAnnotation(colorExt.GetTextField());

                cb.Rectangle(320f, 100f, 240f, 18f); 
                cb.Stroke();
                TextField colorInt = new TextField(writer, new iTextSharp.text.Rectangle(320, 100, 560, 118), "InteriorColor");
                colorInt.Text = cbxIntCol.Text;
                writer.AddAnnotation(colorInt.GetTextField());

                doc.Close();
                writer.Close();
            }

           

        }

        private string GetTextBoxValue(string name)
        {
            var tb = this.Controls.Find(name, true).FirstOrDefault() as TextBox;
            return tb?.Text ?? "";
        }

        private void ClearForm()
        {
            tbxQty1.Text = "";
            tbxQty2.Text = "";
            tbxQty3.Text = "";
            tbxQty4.Text = "";
            tbxQty5.Text = "";
            tbxQty6.Text = "";
            tbxQty7.Text = "";
            tbxQty8.Text = "";

            tbxDesc1.Text = "";
            tbxDesc2.Text = "";
            tbxDesc3.Text = "";
            tbxDesc4.Text = "";
            tbxDesc5.Text = "";
            tbxDesc6.Text = "";
            tbxDesc7.Text = "";
            tbxDesc8.Text = "";

            tbxUOM1.Text = "";
            tbxUOM2.Text = "";
            tbxUOM3.Text = "";
            tbxUOM4.Text = "";
            tbxUOM5.Text = "";
            tbxUOM6.Text = "";
            tbxUOM7.Text = "";
            tbxUOM8.Text = "";

        }

        private void button2_Click(object sender, EventArgs e)
        {
            this.Close();
        }

        private void tbxPO_TextChanged(object sender, EventArgs e)
        {
            if (int.TryParse(tbxPO.Text, out int newPONumber))
            {
                currentPONumber = newPONumber;
                SavePONumber();
            }
        }

        private void cbxExtCol_SelectedIndexChanged(object sender, EventArgs e)
        {

            cbxExtCol.Items.Add("Dal-04 Blanc");

        }

        private void label12_Click(object sender, EventArgs e)
        {

        }
    }
}