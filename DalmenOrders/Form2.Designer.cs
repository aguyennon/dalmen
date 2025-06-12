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
            this.lbl1to7 = new System.Windows.Forms.Label();
            this.lbl8to13 = new System.Windows.Forms.Label();
            this.lblLotResult = new System.Windows.Forms.Label();
            this.lblWasteResult = new System.Windows.Forms.Label();
            this.btnOk = new System.Windows.Forms.Button();
            this.printResults = new System.Drawing.Printing.PrintDocument();
            this.btnPrint = new System.Windows.Forms.Button();
            this.lblDeligneResult = new System.Windows.Forms.Label();
            this.dgv1to7 = new System.Windows.Forms.DataGridView();
            this.dgv8to13 = new System.Windows.Forms.DataGridView();
            this.label1 = new System.Windows.Forms.Label();
            this.label2 = new System.Windows.Forms.Label();
            this.label3 = new System.Windows.Forms.Label();
            this.label4 = new System.Windows.Forms.Label();
            ((System.ComponentModel.ISupportInitialize)(this.dgv1to7)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.dgv8to13)).BeginInit();
            this.SuspendLayout();
            // 
            // lblBoard1
            // 
            this.lblBoard1.AutoSize = true;
            this.lblBoard1.Font = new System.Drawing.Font("Mongolian Baiti", 22.2F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.lblBoard1.Location = new System.Drawing.Point(363, -1);
            this.lblBoard1.Name = "lblBoard1";
            this.lblBoard1.Size = new System.Drawing.Size(128, 40);
            this.lblBoard1.TabIndex = 0;
            this.lblBoard1.Text = "Boards";
            // 
            // lblBoard2
            // 
            this.lblBoard2.AutoSize = true;
            this.lblBoard2.Font = new System.Drawing.Font("Mongolian Baiti", 22.2F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.lblBoard2.Location = new System.Drawing.Point(731, -1);
            this.lblBoard2.Name = "lblBoard2";
            this.lblBoard2.Size = new System.Drawing.Size(128, 40);
            this.lblBoard2.TabIndex = 1;
            this.lblBoard2.Text = "Boards";
            this.lblBoard2.Click += new System.EventHandler(this.lblBoard2_Click);
            // 
            // lbl1to7
            // 
            this.lbl1to7.AutoSize = true;
            this.lbl1to7.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.lbl1to7.Location = new System.Drawing.Point(205, 326);
            this.lbl1to7.Name = "lbl1to7";
            this.lbl1to7.Size = new System.Drawing.Size(30, 25);
            this.lbl1to7.TabIndex = 2;
            this.lbl1to7.Text = "1 ";
            // 
            // lbl8to13
            // 
            this.lbl8to13.AutoSize = true;
            this.lbl8to13.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.lbl8to13.Location = new System.Drawing.Point(989, 309);
            this.lbl8to13.Name = "lbl8to13";
            this.lbl8to13.Size = new System.Drawing.Size(30, 25);
            this.lbl8to13.TabIndex = 3;
            this.lbl8to13.Text = "8 ";
            this.lbl8to13.Click += new System.EventHandler(this.lbl8to13_Click);
            // 
            // lblLotResult
            // 
            this.lblLotResult.AutoSize = true;
            this.lblLotResult.Font = new System.Drawing.Font("Mongolian Baiti", 13.8F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.lblLotResult.Location = new System.Drawing.Point(1, 109);
            this.lblLotResult.Name = "lblLotResult";
            this.lblLotResult.Size = new System.Drawing.Size(79, 24);
            this.lblLotResult.TabIndex = 4;
            this.lblLotResult.Text = "Lot #: ";
            // 
            // lblWasteResult
            // 
            this.lblWasteResult.AutoSize = true;
            this.lblWasteResult.Font = new System.Drawing.Font("Mongolian Baiti", 13.8F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.lblWasteResult.Location = new System.Drawing.Point(1, 640);
            this.lblWasteResult.Name = "lblWasteResult";
            this.lblWasteResult.Size = new System.Drawing.Size(146, 24);
            this.lblWasteResult.TabIndex = 5;
            this.lblWasteResult.Text = "Total Waste: ";
            // 
            // btnOk
            // 
            this.btnOk.BackColor = System.Drawing.SystemColors.InactiveCaption;
            this.btnOk.Location = new System.Drawing.Point(989, 670);
            this.btnOk.Name = "btnOk";
            this.btnOk.Size = new System.Drawing.Size(116, 62);
            this.btnOk.TabIndex = 6;
            this.btnOk.Text = "&OK";
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
            this.btnPrint.Location = new System.Drawing.Point(989, 602);
            this.btnPrint.Name = "btnPrint";
            this.btnPrint.Size = new System.Drawing.Size(116, 62);
            this.btnPrint.TabIndex = 7;
            this.btnPrint.Text = "&PRINT";
            this.btnPrint.UseVisualStyleBackColor = false;
            this.btnPrint.Click += new System.EventHandler(this.btnPrint_Click);
            // 
            // lblDeligneResult
            // 
            this.lblDeligneResult.AutoSize = true;
            this.lblDeligneResult.Font = new System.Drawing.Font("Mongolian Baiti", 13.8F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.lblDeligneResult.Location = new System.Drawing.Point(1, 142);
            this.lblDeligneResult.Name = "lblDeligneResult";
            this.lblDeligneResult.Size = new System.Drawing.Size(129, 24);
            this.lblDeligneResult.TabIndex = 8;
            this.lblDeligneResult.Text = "Déligné À: ";
            // 
            // dgv1to7
            // 
            this.dgv1to7.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            this.dgv1to7.Location = new System.Drawing.Point(238, 42);
            this.dgv1to7.Name = "dgv1to7";
            this.dgv1to7.RowHeadersWidth = 51;
            this.dgv1to7.RowTemplate.Height = 24;
            this.dgv1to7.Size = new System.Drawing.Size(362, 692);
            this.dgv1to7.TabIndex = 9;
            // 
            // dgv8to13
            // 
            this.dgv8to13.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            this.dgv8to13.Location = new System.Drawing.Point(621, 42);
            this.dgv8to13.Name = "dgv8to13";
            this.dgv8to13.RowHeadersWidth = 51;
            this.dgv8to13.RowTemplate.Height = 24;
            this.dgv8to13.Size = new System.Drawing.Size(362, 695);
            this.dgv8to13.TabIndex = 10;
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label1.Location = new System.Drawing.Point(209, 361);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(20, 25);
            this.label1.TabIndex = 11;
            this.label1.Text = "-";
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label2.Location = new System.Drawing.Point(204, 404);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(24, 25);
            this.label2.TabIndex = 12;
            this.label2.Text = "6";
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label3.Location = new System.Drawing.Point(989, 361);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(20, 25);
            this.label3.TabIndex = 13;
            this.label3.Text = "-";
            // 
            // label4
            // 
            this.label4.AutoSize = true;
            this.label4.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label4.Location = new System.Drawing.Point(989, 404);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(36, 25);
            this.label4.TabIndex = 14;
            this.label4.Text = "13";
            // 
            // Form2
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(8F, 16F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.BackColor = System.Drawing.SystemColors.ActiveCaption;
            this.ClientSize = new System.Drawing.Size(1117, 744);
            this.ControlBox = false;
            this.Controls.Add(this.label4);
            this.Controls.Add(this.label3);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.dgv8to13);
            this.Controls.Add(this.dgv1to7);
            this.Controls.Add(this.lblDeligneResult);
            this.Controls.Add(this.btnPrint);
            this.Controls.Add(this.btnOk);
            this.Controls.Add(this.lblWasteResult);
            this.Controls.Add(this.lblLotResult);
            this.Controls.Add(this.lbl8to13);
            this.Controls.Add(this.lbl1to7);
            this.Controls.Add(this.lblBoard2);
            this.Controls.Add(this.lblBoard1);
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
        private System.Windows.Forms.Label lbl1to7;
        private System.Windows.Forms.Label lbl8to13;
        private System.Windows.Forms.Label lblLotResult;
        private System.Windows.Forms.Label lblWasteResult;
        private System.Windows.Forms.Button btnOk;
        private System.Drawing.Printing.PrintDocument printResults;
        private System.Windows.Forms.Button btnPrint;
        private System.Windows.Forms.Label lblDeligneResult;
        private System.Windows.Forms.DataGridView dgv1to7;
        private System.Windows.Forms.DataGridView dgv8to13;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.Label label4;
    }
}