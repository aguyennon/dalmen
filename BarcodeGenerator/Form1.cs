using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Drawing.Printing;
using System.Linq;
using System.Security.Policy;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using ZXing;

namespace BarcodeGenerator
{
    public partial class Form1 : Form
    {
        private PrintDocument printDoc;
        private Bitmap memoryImage;
        public Form1()
        {
            InitializeComponent();
        }

        private void btnGenerate_Click(object sender, EventArgs e)
        {
            if (string.IsNullOrEmpty(tbxCode1.Text) && string.IsNullOrEmpty(tbxCode2.Text) && string.IsNullOrEmpty(tbxCode3.Text) 
                && string.IsNullOrEmpty(tbxCode4.Text))
            {
                MessageBox.Show("Please enter at least one code to generate the barcode(s).");
            }

            try
            {
                BarcodeWriter writer = new BarcodeWriter();
                writer.Format = BarcodeFormat.CODE_128;
                writer.Options = new ZXing.Common.EncodingOptions
                {
                    Height
                    = 50,
                    Width = 500,
                    Margin = 20,
                    PureBarcode = true,
                };

                if (!string.IsNullOrEmpty(tbxCode1.Text))
                {
                    Bitmap barcodeBitmap1 = writer.Write(tbxCode1.Text);
                    pbxBarcode1.Image = barcodeBitmap1;
                }
                else
                {
                    pbxBarcode1.Image = null;
                }

                // Generate barcode for tbxCode2 -> pbxBarcode2
                if (!string.IsNullOrEmpty(tbxCode2.Text))
                {
                    Bitmap barcodeBitmap2 = writer.Write(tbxCode2.Text);
                    pbxBarcode2.Image = barcodeBitmap2;
                }
                else
                {
                    pbxBarcode2.Image = null;
                }

                // Generate barcode for tbxCode3 -> pbxBarcode3
                if (!string.IsNullOrEmpty(tbxCode3.Text))
                {
                   Bitmap barcodeBitmap3 = writer.Write(tbxCode3.Text);
                    pbxBarcode3.Image = barcodeBitmap3;
                }
                else
                {
                    pbxBarcode3.Image = null;
                }

                // Generate barcode for tbxCode4 -> pbxBarcode4
                if (!string.IsNullOrEmpty(tbxCode4.Text))
                {
                    Bitmap barcodeBitmap4 = writer.Write(tbxCode4.Text);
                    pbxBarcode4.Image = barcodeBitmap4;
                }
                else
                {
                    pbxBarcode4.Image = null;
                }

            }
            catch (Exception ex)
            {
                MessageBox.Show("Error generating barcode: " + ex.Message);
            }
        }

        private void SaveBarcode()
        {
            if (pbxBarcode1.Image != null)
            {
                SaveFileDialog saveDialog = new SaveFileDialog();
                saveDialog.Filter = "PNG files (*.png)|*.png";
                saveDialog.DefaultExt = "png";
                saveDialog.FileName = $"barcode_{tbxCode1.Text}";

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

                        pbxBarcode1.Image.Save(saveDialog.FileName, format);
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

        private void SaveBarcode2()
        {
            if (pbxBarcode2.Image != null)
            {
                SaveFileDialog saveDialog = new SaveFileDialog();
                saveDialog.Filter = "PNG files (*.png)|*.png";
                saveDialog.DefaultExt = "png";
                saveDialog.FileName = $"barcode_{tbxCode2.Text}";

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

                        pbxBarcode2.Image.Save(saveDialog.FileName, format);
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

        private void SaveBarcode3()
        {
            if (pbxBarcode3.Image != null)
            {
                SaveFileDialog saveDialog = new SaveFileDialog();
                saveDialog.Filter = "PNG files (*.png)|*.png";
                saveDialog.DefaultExt = "png";
                saveDialog.FileName = $"barcode_{tbxCode3.Text}";

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

                        pbxBarcode3.Image.Save(saveDialog.FileName, format);
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

        private void btnSave_Click(object sender, EventArgs e)
        {
            SaveBarcode();
        }

        private void btnExit_Click(object sender, EventArgs e)
        {
            this.Close();
        }

        private void btnPrint_Click(object sender, EventArgs e)
        {
            PrintDocument printDoc = new PrintDocument();
            printDoc.PrintPage += PrintDoc_PrintPage;

            PrintDialog printDialog = new PrintDialog();
            printDialog.Document = printDoc;

            if (printDialog.ShowDialog() == DialogResult.OK)
            {
                printDoc.Print();
            }
        }

        private void PrintDoc_PrintPage(object sender, PrintPageEventArgs e)
        {
            int yOffset = e.MarginBounds.Top;
            int verticalSpacing = 100; // Increased to account for text
            int horizontalSpacing = 330;
            int bOffset = e.MarginBounds.Bottom;

            // Print first barcode and text
            if (pbxBarcode1.Image != null)
            {
                Bitmap bmp1 = new Bitmap(pbxBarcode1.Width, pbxBarcode1.Height);
                pbxBarcode1.DrawToBitmap(bmp1, new Rectangle(0, 0, pbxBarcode1.Width, pbxBarcode1.Height));
                e.Graphics.DrawImage(bmp1, e.MarginBounds.Left, yOffset);

                // Add text below first barcode
                if (!string.IsNullOrEmpty(tbxCode1.Text))
                {
                    using (Font font = new Font("Arial", 12, FontStyle.Bold))
                    {
                        SizeF textSize = e.Graphics.MeasureString(tbxCode1.Text, font);
                        float textX = e.MarginBounds.Left + (bmp1.Width - textSize.Width) / 2;
                        float textY = yOffset + bmp1.Height + 10; // Increased gap

                        // Draw a background rectangle to make sure text is visible
                        e.Graphics.FillRectangle(Brushes.White, textX - 2, textY - 2, textSize.Width + 4, textSize.Height + 4);
                        e.Graphics.DrawString(tbxCode1.Text, font, Brushes.Black, textX, textY);
                    }
                }

                bmp1.Dispose();
            }

            yOffset += verticalSpacing;
            int xOffset = e.MarginBounds.Left - 130;

            // Print second barcode and text
            if (pbxBarcode2.Image != null)
            {
                Bitmap bmp2 = new Bitmap(pbxBarcode2.Width, pbxBarcode2.Height);
                pbxBarcode2.DrawToBitmap(bmp2, new Rectangle(0, 0, pbxBarcode2.Width, pbxBarcode2.Height));
                e.Graphics.DrawImage(bmp2, xOffset, yOffset);

                // Add text below second barcode
                if (!string.IsNullOrEmpty(tbxCode2.Text))
                {
                    using (Font font = new Font("Arial", 12, FontStyle.Bold))
                    {
                        SizeF textSize = e.Graphics.MeasureString(tbxCode2.Text, font);
                        float textX = xOffset + (bmp2.Width - textSize.Width) / 2;
                        float textY = yOffset + bmp2.Height + 10;

                        // Draw a background rectangle to make sure text is visible
                        e.Graphics.FillRectangle(Brushes.White, textX - 2, textY - 2, textSize.Width + 4, textSize.Height + 4);
                        e.Graphics.DrawString(tbxCode2.Text, font, Brushes.Black, textX, textY);
                    }
                }

                bmp2.Dispose();
                xOffset += horizontalSpacing;
            }

            // Print third barcode and text
            if (pbxBarcode3.Image != null)
            {
                Bitmap bmp3 = new Bitmap(pbxBarcode3.Width, pbxBarcode3.Height);
                pbxBarcode3.DrawToBitmap(bmp3, new Rectangle(0, 0, pbxBarcode3.Width, pbxBarcode3.Height));
                e.Graphics.DrawImage(bmp3, xOffset, yOffset);

                // Add text below third barcode
                if (!string.IsNullOrEmpty(tbxCode3.Text))
                {
                    using (Font font = new Font("Arial", 12, FontStyle.Bold))
                    {
                        SizeF textSize = e.Graphics.MeasureString(tbxCode3.Text, font);
                        float textX = xOffset + (bmp3.Width - textSize.Width) / 2;
                        float textY = yOffset + bmp3.Height + 10;

                        // Draw a background rectangle to make sure text is visible
                        e.Graphics.FillRectangle(Brushes.White, textX - 2, textY - 2, textSize.Width + 4, textSize.Height + 4);
                        e.Graphics.DrawString(tbxCode3.Text, font, Brushes.Black, textX, textY);
                    }
                }

                bmp3.Dispose();
            }

            if (pbxBarcode4.Image != null)
            {
                Bitmap bmp4 = new Bitmap(pbxBarcode4.Width, pbxBarcode4.Height);
                pbxBarcode4.DrawToBitmap(bmp4, new Rectangle(0, 0, pbxBarcode4.Width, pbxBarcode4.Height));
                e.Graphics.DrawImage(bmp4, e.MarginBounds.Left, bOffset);

                // Add text below first barcode
                if (!string.IsNullOrEmpty(tbxCode4.Text))
                {
                    using (Font font = new Font("Arial", 12, FontStyle.Bold))
                    {
                        SizeF textSize = e.Graphics.MeasureString(tbxCode4.Text, font);
                        float textX = e.MarginBounds.Left + (bmp4.Width - textSize.Width) / 2;
                        float textY = bOffset + bmp4.Height + 10; // Increased gap

                        // Draw a background rectangle to make sure text is visible
                        e.Graphics.FillRectangle(Brushes.White, textX - 2, textY - 2, textSize.Width + 4, textSize.Height + 4);
                        e.Graphics.DrawString(tbxCode4.Text, font, Brushes.Black, textX, textY);
                    }
                }

                bmp4.Dispose();
            }
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            printDoc = new PrintDocument();
            printDoc.PrintPage += PrintDoc_PrintPage;
        }

        private void btnSave2_Click(object sender, EventArgs e)
        {
            SaveBarcode2();
        }

        private void btnSave3_Click(object sender, EventArgs e)
        {
            SaveBarcode3();
        }

        private void btnCancel_Click(object sender, EventArgs e)
        {
            tbxCode1.Clear();
            tbxCode2.Clear();
            tbxCode3.Clear();
            tbxCode4.Clear();
            pbxBarcode1.Image = null;
            pbxBarcode2.Image = null;
            pbxBarcode3.Image = null;
            pbxBarcode4.Image = null;
        }
    }
}
