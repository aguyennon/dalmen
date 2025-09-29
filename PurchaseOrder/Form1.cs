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
using System.Xml.Linq;

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
            SaveAsPDF();
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

        private void SaveAsPDF()
        {
            try
            {
                CaptureScreen();

                // Create filename with PO number
                string fileName = $"PO_{currentPONumber}_{DateTime.Now:yyyyMMdd}.png";
                string folderPath = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.MyDocuments), "PurchaseOrders");

                // Create directory if it doesn't exist
                if (!Directory.Exists(folderPath))
                {
                    Directory.CreateDirectory(folderPath);
                }

                string fullPath = Path.Combine(folderPath, fileName);

                // Save as image (PNG format maintains quality)
                memoryImage.Save(fullPath, ImageFormat.Png);


            }
            catch (Exception ex)
            {
                MessageBox.Show($"Error saving PDF: {ex.Message}");

            }
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
    }
}