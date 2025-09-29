namespace BarcodeGenerator
{
    partial class Form1
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
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(Form1));
            this.lblTitle = new System.Windows.Forms.Label();
            this.lblEnterCode = new System.Windows.Forms.Label();
            this.tbxCode1 = new System.Windows.Forms.TextBox();
            this.btnGenerate = new System.Windows.Forms.Button();
            this.pbxBarcode1 = new System.Windows.Forms.PictureBox();
            this.lblGeneratedBarcode = new System.Windows.Forms.Label();
            this.lblDecision = new System.Windows.Forms.Label();
            this.btnSave = new System.Windows.Forms.Button();
            this.btnCancel = new System.Windows.Forms.Button();
            this.btnExit = new System.Windows.Forms.Button();
            this.btnPrint = new System.Windows.Forms.Button();
            this.lblEnterCode2 = new System.Windows.Forms.Label();
            this.tbxCode2 = new System.Windows.Forms.TextBox();
            this.pbxBarcode2 = new System.Windows.Forms.PictureBox();
            this.tbxCode3 = new System.Windows.Forms.TextBox();
            this.lblEnterCode3 = new System.Windows.Forms.Label();
            this.pbxBarcode3 = new System.Windows.Forms.PictureBox();
            this.btnSave2 = new System.Windows.Forms.Button();
            this.btnSave3 = new System.Windows.Forms.Button();
            this.pictureBox1 = new System.Windows.Forms.PictureBox();
            this.pbxBarcode4 = new System.Windows.Forms.PictureBox();
            this.tbxCode4 = new System.Windows.Forms.TextBox();
            this.lblEnterCode4 = new System.Windows.Forms.Label();
            this.label1 = new System.Windows.Forms.Label();
            ((System.ComponentModel.ISupportInitialize)(this.pbxBarcode1)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.pbxBarcode2)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.pbxBarcode3)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.pictureBox1)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.pbxBarcode4)).BeginInit();
            this.SuspendLayout();
            // 
            // lblTitle
            // 
            this.lblTitle.AutoSize = true;
            this.lblTitle.Font = new System.Drawing.Font("Myanmar Text", 21.75F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.lblTitle.Location = new System.Drawing.Point(3, 18);
            this.lblTitle.Name = "lblTitle";
            this.lblTitle.Size = new System.Drawing.Size(335, 51);
            this.lblTitle.TabIndex = 0;
            this.lblTitle.Text = "BARCODE GENERATOR";
            // 
            // lblEnterCode
            // 
            this.lblEnterCode.AutoSize = true;
            this.lblEnterCode.Font = new System.Drawing.Font("Myanmar Text", 9F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.lblEnterCode.Location = new System.Drawing.Point(35, 68);
            this.lblEnterCode.Name = "lblEnterCode";
            this.lblEnterCode.Size = new System.Drawing.Size(180, 21);
            this.lblEnterCode.TabIndex = 1;
            this.lblEnterCode.Text = "Enter your Part Number (TOP):";
            // 
            // tbxCode1
            // 
            this.tbxCode1.Font = new System.Drawing.Font("Myanmar Text", 11.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.tbxCode1.Location = new System.Drawing.Point(39, 92);
            this.tbxCode1.Name = "tbxCode1";
            this.tbxCode1.Size = new System.Drawing.Size(185, 35);
            this.tbxCode1.TabIndex = 2;
            // 
            // btnGenerate
            // 
            this.btnGenerate.BackColor = System.Drawing.Color.MidnightBlue;
            this.btnGenerate.Font = new System.Drawing.Font("Myanmar Text", 12F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.btnGenerate.ForeColor = System.Drawing.SystemColors.ButtonHighlight;
            this.btnGenerate.Location = new System.Drawing.Point(480, 169);
            this.btnGenerate.Name = "btnGenerate";
            this.btnGenerate.Size = new System.Drawing.Size(185, 91);
            this.btnGenerate.TabIndex = 3;
            this.btnGenerate.Text = "&GENERATE";
            this.btnGenerate.UseVisualStyleBackColor = false;
            this.btnGenerate.Click += new System.EventHandler(this.btnGenerate_Click);
            // 
            // pbxBarcode1
            // 
            this.pbxBarcode1.Location = new System.Drawing.Point(29, 248);
            this.pbxBarcode1.Name = "pbxBarcode1";
            this.pbxBarcode1.Size = new System.Drawing.Size(374, 70);
            this.pbxBarcode1.SizeMode = System.Windows.Forms.PictureBoxSizeMode.CenterImage;
            this.pbxBarcode1.TabIndex = 4;
            this.pbxBarcode1.TabStop = false;
            // 
            // lblGeneratedBarcode
            // 
            this.lblGeneratedBarcode.AutoSize = true;
            this.lblGeneratedBarcode.Font = new System.Drawing.Font("Myanmar Text", 9.75F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.lblGeneratedBarcode.Location = new System.Drawing.Point(35, 221);
            this.lblGeneratedBarcode.Name = "lblGeneratedBarcode";
            this.lblGeneratedBarcode.Size = new System.Drawing.Size(258, 24);
            this.lblGeneratedBarcode.TabIndex = 5;
            this.lblGeneratedBarcode.Text = "The Generated Barcode(s) Will Be Below";
            // 
            // lblDecision
            // 
            this.lblDecision.AutoSize = true;
            this.lblDecision.Font = new System.Drawing.Font("Myanmar Text", 9.75F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.lblDecision.Location = new System.Drawing.Point(35, 618);
            this.lblDecision.Name = "lblDecision";
            this.lblDecision.Size = new System.Drawing.Size(141, 24);
            this.lblDecision.TabIndex = 6;
            this.lblDecision.Text = "Do you wish to save?";
            // 
            // btnSave
            // 
            this.btnSave.BackColor = System.Drawing.Color.MidnightBlue;
            this.btnSave.Font = new System.Drawing.Font("Myanmar Text", 9.75F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.btnSave.ForeColor = System.Drawing.SystemColors.ButtonHighlight;
            this.btnSave.Location = new System.Drawing.Point(29, 645);
            this.btnSave.Name = "btnSave";
            this.btnSave.Size = new System.Drawing.Size(111, 57);
            this.btnSave.TabIndex = 7;
            this.btnSave.Text = "&SAVE 1ST BARCODE";
            this.btnSave.UseVisualStyleBackColor = false;
            this.btnSave.Click += new System.EventHandler(this.btnSave_Click);
            // 
            // btnCancel
            // 
            this.btnCancel.BackColor = System.Drawing.Color.MidnightBlue;
            this.btnCancel.Font = new System.Drawing.Font("Myanmar Text", 9.75F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.btnCancel.ForeColor = System.Drawing.SystemColors.ButtonHighlight;
            this.btnCancel.Location = new System.Drawing.Point(115, 775);
            this.btnCancel.Name = "btnCancel";
            this.btnCancel.Size = new System.Drawing.Size(94, 54);
            this.btnCancel.TabIndex = 8;
            this.btnCancel.Text = "&CLEAR";
            this.btnCancel.UseVisualStyleBackColor = false;
            this.btnCancel.Click += new System.EventHandler(this.btnCancel_Click);
            // 
            // btnExit
            // 
            this.btnExit.BackColor = System.Drawing.Color.MidnightBlue;
            this.btnExit.Font = new System.Drawing.Font("Myanmar Text", 9.75F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.btnExit.ForeColor = System.Drawing.SystemColors.ButtonHighlight;
            this.btnExit.Location = new System.Drawing.Point(607, 775);
            this.btnExit.Name = "btnExit";
            this.btnExit.Size = new System.Drawing.Size(97, 54);
            this.btnExit.TabIndex = 9;
            this.btnExit.Text = "E&XIT";
            this.btnExit.UseVisualStyleBackColor = false;
            this.btnExit.Click += new System.EventHandler(this.btnExit_Click);
            // 
            // btnPrint
            // 
            this.btnPrint.BackColor = System.Drawing.Color.MidnightBlue;
            this.btnPrint.Font = new System.Drawing.Font("Myanmar Text", 9.75F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.btnPrint.ForeColor = System.Drawing.SystemColors.ControlLightLight;
            this.btnPrint.Location = new System.Drawing.Point(12, 775);
            this.btnPrint.Name = "btnPrint";
            this.btnPrint.Size = new System.Drawing.Size(97, 54);
            this.btnPrint.TabIndex = 10;
            this.btnPrint.Text = "&PRINT";
            this.btnPrint.UseVisualStyleBackColor = false;
            this.btnPrint.Click += new System.EventHandler(this.btnPrint_Click);
            // 
            // lblEnterCode2
            // 
            this.lblEnterCode2.AutoSize = true;
            this.lblEnterCode2.Font = new System.Drawing.Font("Myanmar Text", 9F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.lblEnterCode2.Location = new System.Drawing.Point(246, 68);
            this.lblEnterCode2.Name = "lblEnterCode2";
            this.lblEnterCode2.Size = new System.Drawing.Size(202, 21);
            this.lblEnterCode2.TabIndex = 11;
            this.lblEnterCode2.Text = "Enter your Part Number (MIDDLE):";
            // 
            // tbxCode2
            // 
            this.tbxCode2.Font = new System.Drawing.Font("Myanmar Text", 11.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.tbxCode2.Location = new System.Drawing.Point(250, 92);
            this.tbxCode2.Name = "tbxCode2";
            this.tbxCode2.Size = new System.Drawing.Size(185, 35);
            this.tbxCode2.TabIndex = 12;
            // 
            // pbxBarcode2
            // 
            this.pbxBarcode2.Location = new System.Drawing.Point(29, 324);
            this.pbxBarcode2.Name = "pbxBarcode2";
            this.pbxBarcode2.Size = new System.Drawing.Size(354, 70);
            this.pbxBarcode2.SizeMode = System.Windows.Forms.PictureBoxSizeMode.StretchImage;
            this.pbxBarcode2.TabIndex = 14;
            this.pbxBarcode2.TabStop = false;
            // 
            // tbxCode3
            // 
            this.tbxCode3.Font = new System.Drawing.Font("Myanmar Text", 11.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.tbxCode3.Location = new System.Drawing.Point(461, 92);
            this.tbxCode3.Name = "tbxCode3";
            this.tbxCode3.Size = new System.Drawing.Size(185, 35);
            this.tbxCode3.TabIndex = 17;
            // 
            // lblEnterCode3
            // 
            this.lblEnterCode3.AutoSize = true;
            this.lblEnterCode3.Font = new System.Drawing.Font("Myanmar Text", 9F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.lblEnterCode3.Location = new System.Drawing.Point(457, 68);
            this.lblEnterCode3.Name = "lblEnterCode3";
            this.lblEnterCode3.Size = new System.Drawing.Size(208, 21);
            this.lblEnterCode3.TabIndex = 16;
            this.lblEnterCode3.Text = "Enter your Part Number (BOTTOM):";
            // 
            // pbxBarcode3
            // 
            this.pbxBarcode3.Location = new System.Drawing.Point(29, 400);
            this.pbxBarcode3.Name = "pbxBarcode3";
            this.pbxBarcode3.Size = new System.Drawing.Size(354, 70);
            this.pbxBarcode3.SizeMode = System.Windows.Forms.PictureBoxSizeMode.StretchImage;
            this.pbxBarcode3.TabIndex = 18;
            this.pbxBarcode3.TabStop = false;
            // 
            // btnSave2
            // 
            this.btnSave2.BackColor = System.Drawing.Color.MidnightBlue;
            this.btnSave2.Font = new System.Drawing.Font("Myanmar Text", 9.75F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.btnSave2.ForeColor = System.Drawing.SystemColors.ButtonHighlight;
            this.btnSave2.Location = new System.Drawing.Point(157, 645);
            this.btnSave2.Name = "btnSave2";
            this.btnSave2.Size = new System.Drawing.Size(111, 57);
            this.btnSave2.TabIndex = 19;
            this.btnSave2.Text = "&SAVE 2ND BARCODE";
            this.btnSave2.UseVisualStyleBackColor = false;
            this.btnSave2.Click += new System.EventHandler(this.btnSave2_Click);
            // 
            // btnSave3
            // 
            this.btnSave3.BackColor = System.Drawing.Color.MidnightBlue;
            this.btnSave3.Font = new System.Drawing.Font("Myanmar Text", 9.75F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.btnSave3.ForeColor = System.Drawing.SystemColors.ButtonHighlight;
            this.btnSave3.Location = new System.Drawing.Point(292, 645);
            this.btnSave3.Name = "btnSave3";
            this.btnSave3.Size = new System.Drawing.Size(111, 57);
            this.btnSave3.TabIndex = 20;
            this.btnSave3.Text = "&SAVE 3RD BARCODE";
            this.btnSave3.UseVisualStyleBackColor = false;
            this.btnSave3.Click += new System.EventHandler(this.btnSave3_Click);
            // 
            // pictureBox1
            // 
            this.pictureBox1.Image = ((System.Drawing.Image)(resources.GetObject("pictureBox1.Image")));
            this.pictureBox1.Location = new System.Drawing.Point(432, 272);
            this.pictureBox1.Name = "pictureBox1";
            this.pictureBox1.Size = new System.Drawing.Size(271, 249);
            this.pictureBox1.SizeMode = System.Windows.Forms.PictureBoxSizeMode.StretchImage;
            this.pictureBox1.TabIndex = 21;
            this.pictureBox1.TabStop = false;
            // 
            // pbxBarcode4
            // 
            this.pbxBarcode4.Location = new System.Drawing.Point(29, 512);
            this.pbxBarcode4.Name = "pbxBarcode4";
            this.pbxBarcode4.Size = new System.Drawing.Size(374, 70);
            this.pbxBarcode4.SizeMode = System.Windows.Forms.PictureBoxSizeMode.AutoSize;
            this.pbxBarcode4.TabIndex = 22;
            this.pbxBarcode4.TabStop = false;
            // 
            // tbxCode4
            // 
            this.tbxCode4.Font = new System.Drawing.Font("Myanmar Text", 11.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.tbxCode4.Location = new System.Drawing.Point(48, 169);
            this.tbxCode4.Name = "tbxCode4";
            this.tbxCode4.Size = new System.Drawing.Size(185, 35);
            this.tbxCode4.TabIndex = 24;
            // 
            // lblEnterCode4
            // 
            this.lblEnterCode4.AutoSize = true;
            this.lblEnterCode4.Font = new System.Drawing.Font("Myanmar Text", 9F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.lblEnterCode4.Location = new System.Drawing.Point(35, 145);
            this.lblEnterCode4.Name = "lblEnterCode4";
            this.lblEnterCode4.Size = new System.Drawing.Size(216, 21);
            this.lblEnterCode4.TabIndex = 23;
            this.lblEnterCode4.Text = "Enter your Part Number (OPTIONAL):";
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.ForeColor = System.Drawing.Color.Red;
            this.label1.Location = new System.Drawing.Point(26, 496);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(311, 13);
            this.label1.TabIndex = 25;
            this.label1.Text = "This barcode is optional and strictly to generate longer barcodes.";
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(715, 841);
            this.ControlBox = false;
            this.Controls.Add(this.label1);
            this.Controls.Add(this.tbxCode4);
            this.Controls.Add(this.lblEnterCode4);
            this.Controls.Add(this.pbxBarcode4);
            this.Controls.Add(this.pictureBox1);
            this.Controls.Add(this.btnSave3);
            this.Controls.Add(this.btnSave2);
            this.Controls.Add(this.pbxBarcode3);
            this.Controls.Add(this.tbxCode3);
            this.Controls.Add(this.lblEnterCode3);
            this.Controls.Add(this.pbxBarcode2);
            this.Controls.Add(this.tbxCode2);
            this.Controls.Add(this.lblEnterCode2);
            this.Controls.Add(this.btnPrint);
            this.Controls.Add(this.btnExit);
            this.Controls.Add(this.btnCancel);
            this.Controls.Add(this.btnSave);
            this.Controls.Add(this.lblDecision);
            this.Controls.Add(this.lblGeneratedBarcode);
            this.Controls.Add(this.pbxBarcode1);
            this.Controls.Add(this.btnGenerate);
            this.Controls.Add(this.tbxCode1);
            this.Controls.Add(this.lblEnterCode);
            this.Controls.Add(this.lblTitle);
            this.Name = "Form1";
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen;
            this.Text = "Barcode Generator";
            this.Load += new System.EventHandler(this.Form1_Load);
            ((System.ComponentModel.ISupportInitialize)(this.pbxBarcode1)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.pbxBarcode2)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.pbxBarcode3)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.pictureBox1)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.pbxBarcode4)).EndInit();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Label lblTitle;
        private System.Windows.Forms.Label lblEnterCode;
        private System.Windows.Forms.TextBox tbxCode1;
        private System.Windows.Forms.Button btnGenerate;
        private System.Windows.Forms.PictureBox pbxBarcode1;
        private System.Windows.Forms.Label lblGeneratedBarcode;
        private System.Windows.Forms.Label lblDecision;
        private System.Windows.Forms.Button btnSave;
        private System.Windows.Forms.Button btnCancel;
        private System.Windows.Forms.Button btnExit;
        private System.Windows.Forms.Button btnPrint;
        private System.Windows.Forms.Label lblEnterCode2;
        private System.Windows.Forms.TextBox tbxCode2;
        private System.Windows.Forms.PictureBox pbxBarcode2;
        private System.Windows.Forms.TextBox tbxCode3;
        private System.Windows.Forms.Label lblEnterCode3;
        private System.Windows.Forms.PictureBox pbxBarcode3;
        private System.Windows.Forms.Button btnSave2;
        private System.Windows.Forms.Button btnSave3;
        private System.Windows.Forms.PictureBox pictureBox1;
        private System.Windows.Forms.PictureBox pbxBarcode4;
        private System.Windows.Forms.TextBox tbxCode4;
        private System.Windows.Forms.Label lblEnterCode4;
        private System.Windows.Forms.Label label1;
    }
}

