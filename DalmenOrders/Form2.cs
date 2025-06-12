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
using System.Text;
using static DalmenOrders.Form1;

namespace DalmenOrders
{
    public partial class Form2 : Form
    {

        private OptimizationResult _result;
        private string _lotNumber;
        private string _deligne;

        public Form2(OptimizationResult result, string lotNumber, string deligne)
        {
            InitializeComponent();
            _result = result;
            _lotNumber = lotNumber;
            _deligne = deligne;
           
        }

        private void PopulateResults()
        {
             lblLotResult.Text = "Lot #: " + _lotNumber;
             lblDeligneResult.Text = "Déligné À: " + _deligne;
             lblWasteResult.Text = "Total Waste: " + _result.TotalWaste.ToString();

             SetupDataGridViews();
             PopulateDataGridViews();
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
            int totalBoards = _result.TotalBoards;
            int midPoint = (totalBoards + 1) / 2;

            var leftBoardsUsage = _result.Usage.Where(u => u.BoardNumber <= midPoint).ToList();
            var rightBoardsUsage = _result.Usage.Where(u => u.BoardNumber > midPoint).ToList();

            PopulateDataGridView(dgv1to7, leftBoardsUsage);
            PopulateDataGridView(dgv8to13, rightBoardsUsage);

            if (leftBoardsUsage.Any())
            {
                int minLeft = leftBoardsUsage.Min(u => u.BoardNumber);
                int maxLeft = leftBoardsUsage.Max(u => u.BoardNumber);
                // You could add a label above dgv1to7 showing "Boards {minLeft} - {maxLeft}"
            }

            if (rightBoardsUsage.Any())
            {
                int minRight = rightBoardsUsage.Min(u => u.BoardNumber);
                int maxRight = rightBoardsUsage.Max(u => u.BoardNumber);
                // You could add a label above dgv8to13 showing "Boards {minRight} - {maxRight}"
            }
        }

        private void PopulateDataGridView(DataGridView dgv, List<StockUsage> usageData)
        {
            dgv.Rows.Clear();
            foreach ( var usage in usageData)
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
    

         
        private string stringToPrint="";
        private void btnPrint_Click(object sender, EventArgs e)
        {
            printResults.DocumentName = "Optimization Results - Lot #" + _lotNumber;
            printResults.Print();
        }

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
    }
}
