namespace DalmenOrders
{
    partial class Form2
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.lblBoard1 = new System.Windows.Forms.Label();
            this.lblBoard2 = new System.Windows.Forms.Label();
            this.lblLotResult = new System.Windows.Forms.Label();
            this.lblWasteResult = new System.Windows.Forms.Label();
            this.btnOk = new System.Windows.Forms.Button();
            this.printResults = new System.Drawing.Printing.PrintDocument();
            this.btnPrint = new System.Windows.Forms.Button();
            this.lblDeligneResult = new System.Windows.Forms.Label();
            this.dgv1to7 = new System.Windows.Forms.DataGridView();
            this.dgv8to13 = new System.Windows.Forms.DataGridView();
            this.btnSecondDelignage = new System.Windows.Forms.Button();
            this.btnExitOut = new System.Windows.Forms.Button();
            ((System.ComponentModel.ISupportInitialize)(this.dgv1to7)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.dgv8to13)).BeginInit();
            this.SuspendLayout();
            // 
            // lblBoard1
            // 
            this.lblBoard1.AutoSize = true;
            this.lblBoard1.Font = new System.Drawing.Font("Mongolian Baiti", 22.2F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.lblBoard1.Location = new System.Drawing.Point(319, 49);
            this.lblBoard1.Margin = new System.Windows.Forms.Padding(2, 0, 2, 0);
            this.lblBoard1.Name = "lblBoard1";
            this.lblBoard1.Size = new System.Drawing.Size(143, 31);
            this.lblBoard1.TabIndex = 0;
            this.lblBoard1.Text = "BOARDS";
            this.lblBoard1.Click += new System.EventHandler(this.lblBoard1_Click);
            // 
            // lblBoard2
            // 
            this.lblBoard2.AutoSize = true;
            this.lblBoard2.Font = new System.Drawing.Font("Mongolian Baiti", 22.2F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.lblBoard2.Location = new System.Drawing.Point(625, 49);
            this.lblBoard2.Margin = new System.Windows.Forms.Padding(2, 0, 2, 0);
            this.lblBoard2.Name = "lblBoard2";
            this.lblBoard2.Size = new System.Drawing.Size(143, 31);
            this.lblBoard2.TabIndex = 1;
            this.lblBoard2.Text = "BOARDS";
            this.lblBoard2.Click += new System.EventHandler(this.lblBoard2_Click);
            // 
            // lblLotResult
            // 
            this.lblLotResult.AutoSize = true;
            this.lblLotResult.Font = new System.Drawing.Font("Mongolian Baiti", 13.8F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.lblLotResult.Location = new System.Drawing.Point(7, 144);
            this.lblLotResult.Margin = new System.Windows.Forms.Padding(2, 0, 2, 0);
            this.lblLotResult.Name = "lblLotResult";
            this.lblLotResult.Size = new System.Drawing.Size(79, 20);
            this.lblLotResult.TabIndex = 4;
            this.lblLotResult.Text = "LOT #: ";
            // 
            // lblWasteResult
            // 
            this.lblWasteResult.AutoSize = true;
            this.lblWasteResult.Font = new System.Drawing.Font("Mongolian Baiti", 13.8F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.lblWasteResult.ForeColor = System.Drawing.Color.Red;
            this.lblWasteResult.Location = new System.Drawing.Point(3, 786);
            this.lblWasteResult.Margin = new System.Windows.Forms.Padding(2, 0, 2, 0);
            this.lblWasteResult.Name = "lblWasteResult";
            this.lblWasteResult.Size = new System.Drawing.Size(168, 20);
            this.lblWasteResult.TabIndex = 5;
            this.lblWasteResult.Text = "WASTE TOTAL: ";
            // 
            // btnOk
            // 
            this.btnOk.BackColor = System.Drawing.SystemColors.InactiveCaption;
            this.btnOk.Location = new System.Drawing.Point(17, 820);
            this.btnOk.Margin = new System.Windows.Forms.Padding(2);
            this.btnOk.Name = "btnOk";
            this.btnOk.Size = new System.Drawing.Size(107, 61);
            this.btnOk.TabIndex = 6;
            this.btnOk.Text = "&Back";
            this.btnOk.UseVisualStyleBackColor = false;
            this.btnOk.Click += new System.EventHandler(this.btnOk_Click);
            // 
            // printResults
            // 
            this.printResults.PrintPage += new System.Drawing.Printing.PrintPageEventHandler(this.printResults_PrintPage);
            // 
            // btnPrint
            // 
            this.btnPrint.BackColor = System.Drawing.SystemColors.InactiveCaption;
            this.btnPrint.Location = new System.Drawing.Point(11, 60);
            this.btnPrint.Margin = new System.Windows.Forms.Padding(2);
            this.btnPrint.Name = "btnPrint";
            this.btnPrint.Size = new System.Drawing.Size(119, 65);
            this.btnPrint.TabIndex = 7;
            this.btnPrint.Text = "&PRINT";
            this.btnPrint.UseVisualStyleBackColor = false;
            this.btnPrint.Click += new System.EventHandler(this.btnPrint_Click);
            // 
            // lblDeligneResult
            // 
            this.lblDeligneResult.AutoSize = true;
            this.lblDeligneResult.Font = new System.Drawing.Font("Mongolian Baiti", 13.8F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.lblDeligneResult.Location = new System.Drawing.Point(3, 189);
            this.lblDeligneResult.Margin = new System.Windows.Forms.Padding(2, 0, 2, 0);
            this.lblDeligneResult.Name = "lblDeligneResult";
            this.lblDeligneResult.Size = new System.Drawing.Size(133, 20);
            this.lblDeligneResult.TabIndex = 8;
            this.lblDeligneResult.Text = "DÉLIGNÉ À: ";
            // 
            // dgv1to7
            // 
            this.dgv1to7.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            this.dgv1to7.Location = new System.Drawing.Point(251, 82);
            this.dgv1to7.Margin = new System.Windows.Forms.Padding(2);
            this.dgv1to7.Name = "dgv1to7";
            this.dgv1to7.RowHeadersWidth = 51;
            this.dgv1to7.RowTemplate.Height = 24;
            this.dgv1to7.Size = new System.Drawing.Size(283, 894);
            this.dgv1to7.TabIndex = 9;
            this.dgv1to7.CellContentClick += new System.Windows.Forms.DataGridViewCellEventHandler(this.dgv1to7_CellContentClick);
            // 
            // dgv8to13
            // 
            this.dgv8to13.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            this.dgv8to13.Location = new System.Drawing.Point(551, 82);
            this.dgv8to13.Margin = new System.Windows.Forms.Padding(2);
            this.dgv8to13.Name = "dgv8to13";
            this.dgv8to13.RowHeadersWidth = 51;
            this.dgv8to13.RowTemplate.Height = 24;
            this.dgv8to13.Size = new System.Drawing.Size(300, 894);
            this.dgv8to13.TabIndex = 10;
            this.dgv8to13.CellContentClick += new System.Windows.Forms.DataGridViewCellEventHandler(this.dgv8to13_CellContentClick);
            // 
            // btnSecondDelignage
            // 
            this.btnSecondDelignage.BackColor = System.Drawing.SystemColors.InactiveCaption;
            this.btnSecondDelignage.Location = new System.Drawing.Point(7, 251);
            this.btnSecondDelignage.Name = "btnSecondDelignage";
            this.btnSecondDelignage.Size = new System.Drawing.Size(113, 56);
            this.btnSecondDelignage.TabIndex = 11;
            this.btnSecondDelignage.Text = "Click Here For Second Delignage!";
            this.btnSecondDelignage.UseVisualStyleBackColor = false;
            this.btnSecondDelignage.Click += new System.EventHandler(this.btnSecondDelignage_Click_1);
            // 
            // btnExitOut
            // 
            this.btnExitOut.BackColor = System.Drawing.SystemColors.InactiveCaption;
            this.btnExitOut.Location = new System.Drawing.Point(17, 895);
            this.btnExitOut.Margin = new System.Windows.Forms.Padding(2);
            this.btnExitOut.Name = "btnExitOut";
            this.btnExitOut.Size = new System.Drawing.Size(107, 61);
            this.btnExitOut.TabIndex = 12;
            this.btnExitOut.Text = "E&xit";
            this.btnExitOut.UseVisualStyleBackColor = false;
            this.btnExitOut.Click += new System.EventHandler(this.btnExitOut_Click);
            // 
            // Form2
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.BackColor = System.Drawing.SystemColors.ActiveCaption;
            this.ClientSize = new System.Drawing.Size(1094, 987);
            this.ControlBox = false;
            this.Controls.Add(this.btnExitOut);
            this.Controls.Add(this.btnSecondDelignage);
            this.Controls.Add(this.dgv8to13);
            this.Controls.Add(this.dgv1to7);
            this.Controls.Add(this.lblDeligneResult);
            this.Controls.Add(this.btnPrint);
            this.Controls.Add(this.btnOk);
            this.Controls.Add(this.lblWasteResult);
            this.Controls.Add(this.lblLotResult);
            this.Controls.Add(this.lblBoard2);
            this.Controls.Add(this.lblBoard1);
            this.Margin = new System.Windows.Forms.Padding(2);
            this.Name = "Form2";
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen;
            this.Text = "Form2";
            this.Load += new System.EventHandler(this.Form2_Load);
            ((System.ComponentModel.ISupportInitialize)(this.dgv1to7)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.dgv8to13)).EndInit();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Label lblBoard1;
        private System.Windows.Forms.Label lblBoard2;
        private System.Windows.Forms.Label lblLotResult;
        private System.Windows.Forms.Label lblWasteResult;
        private System.Windows.Forms.Button btnOk;
        private System.Drawing.Printing.PrintDocument printResults;
        private System.Windows.Forms.Button btnPrint;
        private System.Windows.Forms.Label lblDeligneResult;
        private System.Windows.Forms.DataGridView dgv1to7;
        private System.Windows.Forms.DataGridView dgv8to13;
        private System.Windows.Forms.Button btnSecondDelignage;
        private System.Windows.Forms.Button btnExitOut;
    }
}