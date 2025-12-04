namespace BarcodeGenerator
{
    partial class frmDB
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
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(frmDB));
            this.lblEnter = new System.Windows.Forms.Label();
            this.tbxBarcode = new System.Windows.Forms.TextBox();
            this.btnFetchDesc = new System.Windows.Forms.Button();
            this.btnPrint = new System.Windows.Forms.Button();
            this.btnClear = new System.Windows.Forms.Button();
            this.btnBack = new System.Windows.Forms.Button();
            this.btnExit = new System.Windows.Forms.Button();
            this.btnGenCode = new System.Windows.Forms.Button();
            this.pbxBarcode = new System.Windows.Forms.PictureBox();
            this.btnPrintPaper = new System.Windows.Forms.Button();
            this.btnSaveForLayout = new System.Windows.Forms.Button();
            this.pictureBox1 = new System.Windows.Forms.PictureBox();
            this.btnPDFSaved = new System.Windows.Forms.Button();
            this.gbxDescInfo = new System.Windows.Forms.GroupBox();
            this.lblDescInfo = new System.Windows.Forms.Label();
            this.lblRecordHistory = new System.Windows.Forms.Label();
            ((System.ComponentModel.ISupportInitialize)(this.pbxBarcode)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.pictureBox1)).BeginInit();
            this.gbxDescInfo.SuspendLayout();
            this.SuspendLayout();
            // 
            // lblEnter
            // 
            this.lblEnter.AutoSize = true;
            this.lblEnter.Font = new System.Drawing.Font("Myanmar Text", 14.25F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.lblEnter.Location = new System.Drawing.Point(275, 9);
            this.lblEnter.Name = "lblEnter";
            this.lblEnter.Size = new System.Drawing.Size(170, 34);
            this.lblEnter.TabIndex = 0;
            this.lblEnter.Text = "ENTER BARCODE:";
            // 
            // tbxBarcode
            // 
            this.tbxBarcode.Font = new System.Drawing.Font("Myanmar Text", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.tbxBarcode.Location = new System.Drawing.Point(112, 46);
            this.tbxBarcode.Name = "tbxBarcode";
            this.tbxBarcode.Size = new System.Drawing.Size(490, 37);
            this.tbxBarcode.TabIndex = 1;
            // 
            // btnFetchDesc
            // 
            this.btnFetchDesc.BackColor = System.Drawing.Color.MidnightBlue;
            this.btnFetchDesc.Font = new System.Drawing.Font("Myanmar Text", 12F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.btnFetchDesc.ForeColor = System.Drawing.SystemColors.Control;
            this.btnFetchDesc.Location = new System.Drawing.Point(290, 121);
            this.btnFetchDesc.Name = "btnFetchDesc";
            this.btnFetchDesc.Size = new System.Drawing.Size(213, 71);
            this.btnFetchDesc.TabIndex = 2;
            this.btnFetchDesc.Text = "FETCH DESCRIPTION FROM DATABASE";
            this.btnFetchDesc.UseVisualStyleBackColor = false;
            this.btnFetchDesc.Click += new System.EventHandler(this.btnFetchDesc_Click);
            // 
            // btnPrint
            // 
            this.btnPrint.BackColor = System.Drawing.Color.MidnightBlue;
            this.btnPrint.Font = new System.Drawing.Font("Myanmar Text", 12F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.btnPrint.ForeColor = System.Drawing.SystemColors.Control;
            this.btnPrint.Location = new System.Drawing.Point(127, 521);
            this.btnPrint.Name = "btnPrint";
            this.btnPrint.Size = new System.Drawing.Size(228, 101);
            this.btnPrint.TabIndex = 6;
            this.btnPrint.Text = "&PRINT ON STICKER";
            this.btnPrint.UseVisualStyleBackColor = false;
            this.btnPrint.Click += new System.EventHandler(this.btnPrint_Click);
            // 
            // btnClear
            // 
            this.btnClear.BackColor = System.Drawing.Color.Firebrick;
            this.btnClear.Font = new System.Drawing.Font("Myanmar Text", 12F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.btnClear.ForeColor = System.Drawing.Color.White;
            this.btnClear.Location = new System.Drawing.Point(509, 121);
            this.btnClear.Name = "btnClear";
            this.btnClear.Size = new System.Drawing.Size(134, 71);
            this.btnClear.TabIndex = 8;
            this.btnClear.Text = "&CLEAR";
            this.btnClear.UseVisualStyleBackColor = false;
            this.btnClear.Click += new System.EventHandler(this.btnClear_Click);
            // 
            // btnBack
            // 
            this.btnBack.BackColor = System.Drawing.Color.RoyalBlue;
            this.btnBack.Font = new System.Drawing.Font("Myanmar Text", 12F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.btnBack.ForeColor = System.Drawing.SystemColors.Control;
            this.btnBack.Location = new System.Drawing.Point(12, 796);
            this.btnBack.Name = "btnBack";
            this.btnBack.Size = new System.Drawing.Size(112, 80);
            this.btnBack.TabIndex = 9;
            this.btnBack.Text = "&BACK";
            this.btnBack.UseVisualStyleBackColor = false;
            this.btnBack.Click += new System.EventHandler(this.btnBack_Click);
            // 
            // btnExit
            // 
            this.btnExit.BackColor = System.Drawing.Color.Firebrick;
            this.btnExit.Font = new System.Drawing.Font("Myanmar Text", 12F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.btnExit.ForeColor = System.Drawing.SystemColors.Control;
            this.btnExit.Location = new System.Drawing.Point(596, 796);
            this.btnExit.Name = "btnExit";
            this.btnExit.Size = new System.Drawing.Size(111, 80);
            this.btnExit.TabIndex = 10;
            this.btnExit.Text = "E&XIT";
            this.btnExit.UseVisualStyleBackColor = false;
            this.btnExit.Click += new System.EventHandler(this.btnExit_Click);
            // 
            // btnGenCode
            // 
            this.btnGenCode.BackColor = System.Drawing.Color.MidnightBlue;
            this.btnGenCode.Font = new System.Drawing.Font("Myanmar Text", 12F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.btnGenCode.ForeColor = System.Drawing.SystemColors.Control;
            this.btnGenCode.Location = new System.Drawing.Point(69, 121);
            this.btnGenCode.Name = "btnGenCode";
            this.btnGenCode.Size = new System.Drawing.Size(215, 71);
            this.btnGenCode.TabIndex = 11;
            this.btnGenCode.Text = "GENERATE BARCODE";
            this.btnGenCode.UseVisualStyleBackColor = false;
            this.btnGenCode.Click += new System.EventHandler(this.btnGenCode_Click);
            // 
            // pbxBarcode
            // 
            this.pbxBarcode.Location = new System.Drawing.Point(69, 203);
            this.pbxBarcode.Name = "pbxBarcode";
            this.pbxBarcode.Size = new System.Drawing.Size(574, 84);
            this.pbxBarcode.SizeMode = System.Windows.Forms.PictureBoxSizeMode.StretchImage;
            this.pbxBarcode.TabIndex = 23;
            this.pbxBarcode.TabStop = false;
            // 
            // btnPrintPaper
            // 
            this.btnPrintPaper.BackColor = System.Drawing.Color.MidnightBlue;
            this.btnPrintPaper.Font = new System.Drawing.Font("Myanmar Text", 12F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.btnPrintPaper.ForeColor = System.Drawing.SystemColors.Control;
            this.btnPrintPaper.Location = new System.Drawing.Point(361, 521);
            this.btnPrintPaper.Name = "btnPrintPaper";
            this.btnPrintPaper.Size = new System.Drawing.Size(226, 101);
            this.btnPrintPaper.TabIndex = 24;
            this.btnPrintPaper.Text = "P&RINT ON PAPER";
            this.btnPrintPaper.UseVisualStyleBackColor = false;
            this.btnPrintPaper.Click += new System.EventHandler(this.btnPrintPaper_Click);
            // 
            // btnSaveForLayout
            // 
            this.btnSaveForLayout.BackColor = System.Drawing.Color.MidnightBlue;
            this.btnSaveForLayout.Font = new System.Drawing.Font("Myanmar Text", 12F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.btnSaveForLayout.ForeColor = System.Drawing.SystemColors.Control;
            this.btnSaveForLayout.Location = new System.Drawing.Point(127, 414);
            this.btnSaveForLayout.Name = "btnSaveForLayout";
            this.btnSaveForLayout.Size = new System.Drawing.Size(228, 101);
            this.btnSaveForLayout.TabIndex = 25;
            this.btnSaveForLayout.Text = "&SAVE FOR LAYOUT (MAX 7)";
            this.btnSaveForLayout.UseVisualStyleBackColor = false;
            this.btnSaveForLayout.Click += new System.EventHandler(this.btnSaveForLayout_Click);
            // 
            // pictureBox1
            // 
            this.pictureBox1.Image = ((System.Drawing.Image)(resources.GetObject("pictureBox1.Image")));
            this.pictureBox1.Location = new System.Drawing.Point(168, 628);
            this.pictureBox1.Name = "pictureBox1";
            this.pictureBox1.Size = new System.Drawing.Size(380, 162);
            this.pictureBox1.SizeMode = System.Windows.Forms.PictureBoxSizeMode.CenterImage;
            this.pictureBox1.TabIndex = 26;
            this.pictureBox1.TabStop = false;
            // 
            // btnPDFSaved
            // 
            this.btnPDFSaved.BackColor = System.Drawing.Color.MidnightBlue;
            this.btnPDFSaved.Font = new System.Drawing.Font("Myanmar Text", 12F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.btnPDFSaved.ForeColor = System.Drawing.SystemColors.Control;
            this.btnPDFSaved.Location = new System.Drawing.Point(361, 414);
            this.btnPDFSaved.Name = "btnPDFSaved";
            this.btnPDFSaved.Size = new System.Drawing.Size(226, 101);
            this.btnPDFSaved.TabIndex = 27;
            this.btnPDFSaved.Text = "SAVE BARCODES TO PDF";
            this.btnPDFSaved.UseVisualStyleBackColor = false;
            this.btnPDFSaved.Click += new System.EventHandler(this.btnPDFSaved_Click);
            // 
            // gbxDescInfo
            // 
            this.gbxDescInfo.Controls.Add(this.lblDescInfo);
            this.gbxDescInfo.Font = new System.Drawing.Font("Myanmar Text", 9.75F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.gbxDescInfo.Location = new System.Drawing.Point(69, 293);
            this.gbxDescInfo.Name = "gbxDescInfo";
            this.gbxDescInfo.Size = new System.Drawing.Size(574, 98);
            this.gbxDescInfo.TabIndex = 28;
            this.gbxDescInfo.TabStop = false;
            this.gbxDescInfo.Text = "DESCRIPTION";
            // 
            // lblDescInfo
            // 
            this.lblDescInfo.AutoSize = true;
            this.lblDescInfo.Font = new System.Drawing.Font("Myanmar Text", 11.25F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.lblDescInfo.Location = new System.Drawing.Point(94, 38);
            this.lblDescInfo.Name = "lblDescInfo";
            this.lblDescInfo.Size = new System.Drawing.Size(228, 27);
            this.lblDescInfo.TabIndex = 0;
            this.lblDescInfo.Text = "The description will show here.";
            // 
            // lblRecordHistory
            // 
            this.lblRecordHistory.AutoSize = true;
            this.lblRecordHistory.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.75F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.lblRecordHistory.ForeColor = System.Drawing.Color.Red;
            this.lblRecordHistory.Location = new System.Drawing.Point(109, 86);
            this.lblRecordHistory.Name = "lblRecordHistory";
            this.lblRecordHistory.Size = new System.Drawing.Size(203, 16);
            this.lblRecordHistory.TabIndex = 29;
            this.lblRecordHistory.Text = "Last Recorded Saved Code:";
            this.lblRecordHistory.Click += new System.EventHandler(this.lblRecordHistory_Click);
            // 
            // frmDB
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.AutoSize = true;
            this.AutoValidate = System.Windows.Forms.AutoValidate.EnableAllowFocusChange;
            this.BackColor = System.Drawing.SystemColors.ButtonHighlight;
            this.ClientSize = new System.Drawing.Size(719, 888);
            this.Controls.Add(this.lblRecordHistory);
            this.Controls.Add(this.btnSaveForLayout);
            this.Controls.Add(this.btnPDFSaved);
            this.Controls.Add(this.gbxDescInfo);
            this.Controls.Add(this.pictureBox1);
            this.Controls.Add(this.btnPrintPaper);
            this.Controls.Add(this.pbxBarcode);
            this.Controls.Add(this.btnGenCode);
            this.Controls.Add(this.btnExit);
            this.Controls.Add(this.btnBack);
            this.Controls.Add(this.btnClear);
            this.Controls.Add(this.btnPrint);
            this.Controls.Add(this.btnFetchDesc);
            this.Controls.Add(this.tbxBarcode);
            this.Controls.Add(this.lblEnter);
            this.Name = "frmDB";
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen;
            this.Text = "Load Longer Barcodes From Database";
            this.Load += new System.EventHandler(this.frmDB_Load);
            ((System.ComponentModel.ISupportInitialize)(this.pbxBarcode)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.pictureBox1)).EndInit();
            this.gbxDescInfo.ResumeLayout(false);
            this.gbxDescInfo.PerformLayout();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Label lblEnter;
        private System.Windows.Forms.TextBox tbxBarcode;
        private System.Windows.Forms.Button btnFetchDesc;
        private System.Windows.Forms.Button btnPrint;
        private System.Windows.Forms.Button btnClear;
        private System.Windows.Forms.Button btnBack;
        private System.Windows.Forms.Button btnExit;
        private System.Windows.Forms.Button btnGenCode;
        private System.Windows.Forms.PictureBox pbxBarcode;
        private System.Windows.Forms.Button btnPrintPaper;
        private System.Windows.Forms.Button btnSaveForLayout;
        private System.Windows.Forms.PictureBox pictureBox1;
        private System.Windows.Forms.Button btnPDFSaved;
        private System.Windows.Forms.GroupBox gbxDescInfo;
        private System.Windows.Forms.Label lblDescInfo;
        private System.Windows.Forms.Label lblRecordHistory;
    }
}