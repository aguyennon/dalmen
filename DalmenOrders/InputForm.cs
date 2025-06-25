using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace DalmenOrders
{
    public partial class InputForm : Form
    {
        public List<CutItem> ProcessedCuts { get; set; }
        public bool DataProcessed { get; set; }

        private readonly string DatabaseFolderPath = @"Q:\Quotes\FichierDeScie\Soufflage";
        private readonly string DatabaseExtension = ".mdb";

        public InputForm()
        {
            InitializeComponent();
            InitializeComponents();
            ProcessedCuts = new List<CutItem>();
            DataProcessed = false;
        }

        private void InitializeComponents()
        {
            this.txtLengthInput = new System.Windows.Forms.TextBox();
            this.btnProcess = new System.Windows.Forms.Button();
            this.btnCancel = new System.Windows.Forms.Button();
            this.lblInstructions = new System.Windows.Forms.Label();
            this.lblTitle = new System.Windows.Forms.Label();
            this.SuspendLayout();

           
            // lblTitle
            this.lblTitle.AutoSize = true;
            this.lblTitle.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.lblTitle.Location = new System.Drawing.Point(12, 9);
            this.lblTitle.Name = "lblTitle";
            this.lblTitle.Size = new System.Drawing.Size(203, 20);
            this.lblTitle.TabIndex = 0;
            this.lblTitle.Text = "Dalmen Cut List Processor";

            // 
            // lblInstructions
            // 
            this.lblInstructions.AutoSize = true;
            this.lblInstructions.Location = new System.Drawing.Point(12, 40);
            this.lblInstructions.Name = "lblInstructions";
            this.lblInstructions.Size = new System.Drawing.Size(380, 26);
            this.lblInstructions.TabIndex = 1;
            this.lblInstructions.Text = "Paste or enter your cut lengths below (one per line):\r\nThe system will automatically count duplicates and sort by length.";

            // 
            // txtLengthInput
            // 
            this.txtLengthInput.Font = new System.Drawing.Font("Consolas", 10F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.txtLengthInput.Location = new System.Drawing.Point(12, 80);
            this.txtLengthInput.Multiline = true;
            this.txtLengthInput.Name = "txtLengthInput";
            this.txtLengthInput.ScrollBars = System.Windows.Forms.ScrollBars.Vertical;
            this.txtLengthInput.Size = new System.Drawing.Size(460, 250);
            this.txtLengthInput.TabIndex = 2;
            // this.txtLengthInput.Text = "Example:\r\n2400\r\n1800\r\n2400\r\n1200\r\n1800\r\n2400";

            // 
            // btnProcess
            // 
            this.btnProcess.BackColor = System.Drawing.Color.SteelBlue;
            this.btnProcess.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.btnProcess.ForeColor = System.Drawing.Color.White;
            this.btnProcess.Location = new System.Drawing.Point(290, 350);
            this.btnProcess.Name = "btnProcess";
            this.btnProcess.Size = new System.Drawing.Size(90, 35);
            this.btnProcess.TabIndex = 3;
            this.btnProcess.Text = "PROCESS";
            this.btnProcess.UseVisualStyleBackColor = false;
            this.btnProcess.Click += new System.EventHandler(this.btnProcess_Click);

            // 
            // btnCancel
            // 
            this.btnCancel.Location = new System.Drawing.Point(390, 350);
            this.btnCancel.Name = "btnCancel";
            this.btnCancel.Size = new System.Drawing.Size(82, 35);
            this.btnCancel.TabIndex = 4;
            this.btnCancel.Text = "Cancel";
            this.btnCancel.UseVisualStyleBackColor = true;
            this.btnCancel.Click += new System.EventHandler(this.btnCancel_Click);

            // 
            // InputForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(484, 397);
            this.Controls.Add(this.btnCancel);
            this.Controls.Add(this.btnProcess);
            this.Controls.Add(this.txtLengthInput);
            this.Controls.Add(this.lblInstructions);
            this.Controls.Add(this.lblTitle);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedDialog;
            this.MaximizeBox = false;
            this.MinimizeBox = false;
            this.Name = "InputForm";
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen;
            this.Text = "Cut Length Input - Dalmen";
            this.ResumeLayout(false);
            this.PerformLayout();

            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedDialog;
            this.MaximizeBox = false;
            this.MinimizeBox = false;
            this.ShowInTaskbar = false;
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterParent;
            this.TopMost = true;
            this.Name = "InputForm";
            this.Text = "Cut Length Input - Dalmen";
        }

        private System.Windows.Forms.TextBox txtLengthInput;
        private System.Windows.Forms.Button btnProcess;
        private System.Windows.Forms.Button btnCancel;
        private System.Windows.Forms.Label lblInstructions;
        private System.Windows.Forms.Label lblTitle;



        private void btnProcess_Click(object sender, EventArgs e)
        {
            try
            {
                // Get all lines from the textbox
                string[] lines = txtLengthInput.Text.Split(new string[] { "\r\n", "\r", "\n" }, StringSplitOptions.RemoveEmptyEntries);

                // Parse lengths, skip non-numeric lines
                List<double> allLengths = new List<double>();
                foreach (string line in lines)
                {
                    string cleanLine = line.Trim();
                    if (!string.IsNullOrEmpty(cleanLine))
                    {
                        if (double.TryParse(cleanLine, out double length) && length > 0)
                        {
                            allLengths.Add(length);
                        }
                    }
                }

                if (allLengths.Count == 0)
                {
                    MessageBox.Show("No valid lengths found. Please enter numeric values greater than 0.", "Invalid Input", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                    return;
                }

                // Group by length and count occurrences (like the VBA code)
                var groupedLengths = allLengths
                    .GroupBy(length => length)
                    .Select(group => new CutItem
                    {
                        Length = group.Key,
                        Quantity = group.Count()
                    })
                    .OrderByDescending(item => item.Length) // Sort descending like VBA
                    .ToList();

                ProcessedCuts = groupedLengths;
                DataProcessed = true;

                // Show summary
                StringBuilder summary = new StringBuilder();
                summary.AppendLine($"Processed {allLengths.Count} total lengths into {ProcessedCuts.Count} unique cuts:");
                summary.AppendLine();
                foreach (var cut in ProcessedCuts)
                {
                    summary.AppendLine($"Length: {cut.Length} mm - Quantity: {cut.Quantity}");
                }

                MessageBox.Show(summary.ToString(), "Processing Complete", MessageBoxButtons.OK, MessageBoxIcon.Information);

                this.DialogResult = DialogResult.OK;
                this.Close();
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Error processing lengths: {ex.Message}", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void btnCancel_Click(object sender, EventArgs e)
        {
            this.DialogResult = DialogResult.Cancel;
            this.Close();
        }

        private void InputForm_Load(object sender, EventArgs e)
        {
            if (DataProcessed && ProcessedCuts != null && ProcessedCuts.Count > 0)
            {
                StringBuilder sb = new StringBuilder();
                foreach (var cut in ProcessedCuts)
                {
                    sb.AppendLine(cut.Length.ToString());
                }

                txtLengthInput.Text = sb.ToString();
            }
            MessageBox.Show($"Received {ProcessedCuts.Count} cuts");

        }

        public void InitializeCuts()
        {
            if (DataProcessed && ProcessedCuts != null && ProcessedCuts.Count > 0)
            {
                StringBuilder sb = new StringBuilder();
                foreach (var cut in ProcessedCuts)
                {
                    sb.AppendLine(cut.Length.ToString());
                }

                txtLengthInput.Text = sb.ToString(); // Replace with your multiline textbox name
            }
        }

    }

}