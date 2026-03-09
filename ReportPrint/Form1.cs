using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Drawing.Printing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace ReportPrint
{
    public partial class frmMain : Form
    {
        private PrintDocument printDoc = new PrintDocument();
        private Bitmap memoryImage;
        public frmMain()
        {
            InitializeComponent();
            printDoc.PrintPage += new PrintPageEventHandler(PrintDocument_PrintPage);
        }

        private void PrintFormContents()
        {
            // Capture only the visible client area (inside form borders)
            Rectangle bounds = this.RectangleToScreen(this.ClientRectangle);
            memoryImage = new Bitmap(this.ClientSize.Width, this.ClientSize.Height);

            using (Graphics g = Graphics.FromImage(memoryImage))
            {
                g.CopyFromScreen(bounds.Location, Point.Empty, this.ClientSize);
            }

            // Remove printer margins entirely
            printDoc.DefaultPageSettings.Margins = new Margins(0, 0, 0, 0);
            printDoc.OriginAtMargins = false;
            printDoc.DefaultPageSettings.Landscape = false; 

            printDoc.Print();
        }

        private void PrintDocument_PrintPage(object sender, PrintPageEventArgs e)
        {
            // Get printable area
            Rectangle pageArea = e.PageBounds;

            // Scale image to fill entire page (proportionally)
            float scale = Math.Min(
                (float)pageArea.Width / memoryImage.Width,
                (float)pageArea.Height / memoryImage.Height
            );

            int printWidth = (int)(memoryImage.Width * scale);
            int printHeight = (int)(memoryImage.Height * scale);

            // Center it (no white border)
            int x = (pageArea.Width - printWidth) / 2;
            int y = (pageArea.Height - printHeight) / 2;

            e.Graphics.DrawImage(memoryImage, x, y, printWidth, printHeight);
        }

        private void frmMain_Load(object sender, EventArgs e)
        {

        }

        private void label11_Click(object sender, EventArgs e)
        {

        }

        private void btnSave_Click(object sender, EventArgs e)
        {
            PrintFormContents();
        }
    }
}
