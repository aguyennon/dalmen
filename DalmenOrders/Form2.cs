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
using static DalmenOrders.Form1;

namespace DalmenOrders
{
    public partial class Form2 : Form
    {
        private OptimizationResult _primaryResult;
        private OptimizationResult _secondaryResult;
        private string _lotNumber;
        private string _primaryDeligne;
        private string _secondaryDeligne;

        // Constructor for backward compatibility (single delignage)
        public Form2(OptimizationResult result, string lotNumber, string deligne)
        {
            InitializeComponent();
            _primaryResult = result;
            _secondaryResult = null;
            _lotNumber = lotNumber;
            _primaryDeligne = deligne;
            _secondaryDeligne = null;
        }

        // New constructor for multiple delignage support
        public Form2(OptimizationResult primaryResult, OptimizationResult secondaryResult, string lotNumber, string primaryDeligne, string secondaryDeligne)
        {
            InitializeComponent();
            _primaryResult = primaryResult;
            _secondaryResult = secondaryResult;
            _lotNumber = lotNumber;
            _primaryDeligne = primaryDeligne;
            _secondaryDeligne = secondaryDeligne;
        }

        private void PopulateResults()
        {
            lblLotResult.Text = "Lot #: \n" + _lotNumber;
            lblDeligneResult.Text = "Déligné à: \n" + _primaryDeligne;
            lblWasteResult.Text = "Total Waste: \n" + _primaryResult.TotalWaste.ToString();

            SetupDataGridViews();
            PopulateDataGridViews();

            // Show/hide the second delignage button based on whether we have secondary results
            if (_secondaryResult != null && !string.IsNullOrEmpty(_secondaryDeligne))
            {
                btnSecondDelignage.Visible = true;
                btnSecondDelignage.Text = $"View Second Delignage ({_secondaryDeligne})";
            }
            else
            {
               btnSecondDelignage.Visible = false;
            }
        }

        private void SetupDataGridViews()
        {
            SetupDataGridView(dgv1to7);
            SetupDataGridView(dgv8to13);
        }

        private void SetupDataGridView(DataGridView dgv)
        {
            dgv.Columns.Clear();
            dgv.AutoGenerateColumns = false;
            dgv.AllowUserToAddRows = false;
            dgv.AllowUserToDeleteRows = false;
            dgv.ReadOnly = true;
            dgv.SelectionMode = DataGridViewSelectionMode.FullRowSelect;
            dgv.MultiSelect = false;
            dgv.RowHeadersVisible = false;
            dgv.DefaultCellStyle.Font = new Font("Arial", 9, FontStyle.Regular);
            dgv.RowTemplate.Height = 20;

            dgv.Columns.Add(new DataGridViewTextBoxColumn()
            {
                Name = "Board No.",
                HeaderText = "Board No.",
                Width = 70,
                DefaultCellStyle = new DataGridViewCellStyle() { Alignment = DataGridViewContentAlignment.MiddleCenter }
            });

            dgv.Columns.Add(new DataGridViewTextBoxColumn()
            {
                Name = "StockLength",
                HeaderText = "Stock Length",
                Width = 85,
                DefaultCellStyle = new DataGridViewCellStyle() { Alignment = DataGridViewContentAlignment.MiddleCenter }
            });

            dgv.Columns.Add(new DataGridViewTextBoxColumn()
            {
                Name = "CutLength",
                HeaderText = "Cut Length",
                Width = 100,
                DefaultCellStyle = new DataGridViewCellStyle() { Alignment = DataGridViewContentAlignment.MiddleCenter }
            });

            // Style the header
            dgv.ColumnHeadersDefaultCellStyle.BackColor = Color.Navy;
            dgv.ColumnHeadersDefaultCellStyle.ForeColor = Color.White;
            dgv.ColumnHeadersDefaultCellStyle.Font = new Font("Arial", 9, FontStyle.Bold);
            dgv.ColumnHeadersDefaultCellStyle.Alignment = DataGridViewContentAlignment.MiddleCenter;
            dgv.EnableHeadersVisualStyles = false;
            dgv.ColumnHeadersHeight = 25;

            // Alternate row colors for better readability
            dgv.AlternatingRowsDefaultCellStyle.BackColor = Color.LightGray;
            dgv.DefaultCellStyle.BackColor = Color.White;
        }

        private void PopulateDataGridViews()
        {
            int totalBoards = _primaryResult.TotalBoards;
            int midPoint = (totalBoards + 1) / 2;

            var leftBoardsUsage = _primaryResult.Usage.Where(u => u.BoardNumber <= midPoint).ToList();
            var rightBoardsUsage = _primaryResult.Usage.Where(u => u.BoardNumber > midPoint).ToList();

            PopulateDataGridView(dgv1to7, leftBoardsUsage);
            PopulateDataGridView(dgv8to13, rightBoardsUsage);
        }

        private void PopulateDataGridView(DataGridView dgv, List<StockUsage> usageData)
        {
            dgv.Rows.Clear();
            foreach (var usage in usageData)
            {
                string cutDisplay = usage.IsWaste ?
                    usage.CutLength.ToString() + " Waste" :
                    usage.CutLength.ToString();

                int rowIndex = dgv.Rows.Add(
                    usage.BoardNumber,
                    usage.StockLength,
                    cutDisplay
                );

                if (usage.IsWaste)
                {
                    dgv.Rows[rowIndex].DefaultCellStyle.BackColor = Color.LightCoral;
                    dgv.Rows[rowIndex].DefaultCellStyle.ForeColor = Color.DarkRed;
                    dgv.Rows[rowIndex].DefaultCellStyle.Font = new Font("Arial", 9, FontStyle.Italic);
                }
            }

            dgv.AutoResizeColumns(DataGridViewAutoSizeColumnsMode.AllCells);
        }

        private void btnPrint_Click(object sender, EventArgs e)
        {
            printResults.DocumentName = "Optimization Results - Lot #" + _lotNumber;
            printResults.Print();
        }

        // For the 2nd delignage results, need to make it so it prints the popup form, not the Form2
        private void printResults_PrintPage(object sender, System.Drawing.Printing.PrintPageEventArgs e)
        {
            Bitmap formBitmap = new Bitmap(this.Width, this.Height);
            this.DrawToBitmap(formBitmap, new Rectangle(0, 0, this.Width, this.Height));

            float scaleX = (float)e.MarginBounds.Width / formBitmap.Width;
            float scaleY = (float)e.MarginBounds.Height / formBitmap.Height;
            float scale = Math.Min(scaleX, scaleY);

            int scaledWidth = (int)(formBitmap.Width * scale);
            int scaledHeight = (int)(formBitmap.Height * scale);
            int x = e.MarginBounds.Left + (e.MarginBounds.Width - scaledWidth) / 2;
            int y = e.MarginBounds.Top;

            e.Graphics.DrawImage(formBitmap, new Rectangle(x, y, scaledWidth, scaledHeight));

            formBitmap.Dispose();
            e.HasMorePages = false;
        }

        private void btnOk_Click(object sender, EventArgs e)
        {
            this.Close();
        }

        private void Form2_Load(object sender, EventArgs e)
        {
            PopulateResults();
            this.Text = "Optimization Results - Lot #" + _lotNumber;
        }

        private void lbl8to13_Click(object sender, EventArgs e)
        {

        }

        private void lblBoard2_Click(object sender, EventArgs e)
        {

        }

        private void btnSecondDelignage_Click_1(object sender, EventArgs e)
        {
            // Create a popup form to show the second delignage results
            Form secondDelignageForm = new Form();
            secondDelignageForm.Text = $"Second Delignage Results - {_secondaryDeligne}";
            secondDelignageForm.Size = new Size(854, 1015);
            secondDelignageForm.StartPosition = FormStartPosition.CenterParent;

            // Create labels for the second delignage info
            Label lblLot = new Label();
            lblLot.Text = "Lot #: " + _lotNumber;
            lblLot.Location = new Point(20, 20);
            lblLot.Size = new Size(200, 30);
            secondDelignageForm.Controls.Add(lblLot);

            Label lblDeligne = new Label();
            lblDeligne.Text = "Déligné à: " + _secondaryDeligne;
            lblDeligne.Location = new Point(20, 60);
            lblDeligne.Size = new Size(200, 30);
            secondDelignageForm.Controls.Add(lblDeligne);

            Label lblWaste = new Label();
            lblWaste.Text = "Total Waste: " + _secondaryResult.TotalWaste.ToString();
            lblWaste.Location = new Point(20, 100);
            lblWaste.Size = new Size(200, 30);
            secondDelignageForm.Controls.Add(lblWaste);

            // Create DataGridViews for the second delignage
            DataGridView dgvLeft = new DataGridView();
            dgvLeft.Location = new Point(20, 150);
            dgvLeft.Size = new Size(282, 831);
            SetupDataGridView(dgvLeft);

            DataGridView dgvRight = new DataGridView();
            dgvRight.Location = new Point(400, 150);
            dgvRight.Size = new Size(282, 831);
            SetupDataGridView(dgvRight);                                                  

            // Populate the DataGridViews with secondary results
            int totalBoards = _secondaryResult.TotalBoards;
            int midPoint = (totalBoards + 1) / 2;

            var leftBoardsUsage = _secondaryResult.Usage.Where(u => u.BoardNumber <= midPoint).ToList();
            var rightBoardsUsage = _secondaryResult.Usage.Where(u => u.BoardNumber > midPoint).ToList();

            PopulateDataGridView(dgvLeft, leftBoardsUsage);                                        // Can't be same as first one
            PopulateDataGridView(dgvRight, rightBoardsUsage);                                      // Can't be same as first one

            secondDelignageForm.Controls.Add(dgvLeft);
            secondDelignageForm.Controls.Add(dgvRight);

            // Add a close button
            Button btnClose = new Button();
            btnClose.Text = "Close";
            btnClose.Size = new Size(100, 30);
            btnClose.Location = new Point(225, 10);
            btnClose.Click += (s, ev) => secondDelignageForm.Close();
            secondDelignageForm.Controls.Add(btnClose);

            // Add a print button
            Button btnPrint = new Button();
            btnPrint.Text = "Print";
            btnPrint.Size = new Size(100, 30);
            btnPrint.Location = new Point(350, 10);
            btnPrint.Click += (s, ev) =>
            {
                printResults.DocumentName = "Second Delignage Results - Lot #" + _lotNumber;
                printResults.Print();
            };
            secondDelignageForm.Controls.Add(btnPrint);

            // Show the popup
            secondDelignageForm.ShowDialog(this);
        }

        private void btnExitOut_Click(object sender, EventArgs e)
        {
            Application.Exit();

        }
    }
}