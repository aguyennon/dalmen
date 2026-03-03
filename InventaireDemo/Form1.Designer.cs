namespace InventaireDemo
{
    partial class frmMain
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
            this.dgvInventaire = new System.Windows.Forms.DataGridView();
            this.gbxFilters = new System.Windows.Forms.GroupBox();
            this.comboBox1 = new System.Windows.Forms.ComboBox();
            this.lblFiltre = new System.Windows.Forms.Label();
            this.lblRecherche = new System.Windows.Forms.Label();
            this.comboBox2 = new System.Windows.Forms.ComboBox();
            this.pnlLeft = new System.Windows.Forms.Panel();
            this.btnInventaire = new System.Windows.Forms.Button();
            this.btnFournisseurs = new System.Windows.Forms.Button();
            this.btnCategories = new System.Windows.Forms.Button();
            this.btnCommandes = new System.Windows.Forms.Button();
            this.btnPrevisions = new System.Windows.Forms.Button();
            this.btnLocalisation = new System.Windows.Forms.Button();
            this.btnAjouter = new System.Windows.Forms.Button();
            this.btnSupprimer = new System.Windows.Forms.Button();
            this.btnModifier = new System.Windows.Forms.Button();
            this.btnImprimer = new System.Windows.Forms.Button();
            this.btnComm = new System.Windows.Forms.Button();
            this.btnRes = new System.Windows.Forms.Button();
            this.btnPrev = new System.Windows.Forms.Button();
            this.cbxValeur = new System.Windows.Forms.CheckBox();
            this.lblPieces = new System.Windows.Forms.Label();
            this.tbxPieces = new System.Windows.Forms.TextBox();
            this.Category = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.Code = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.Description = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.QuantityinHand = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.QuantityRes = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.QuantityOrder = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.QuantityMinimal = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.UOM = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.Fournisseur = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.QuantityEco = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.Delays = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.Price = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.Moyenne = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.QuantityProductEst = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.Cost = new System.Windows.Forms.DataGridViewTextBoxColumn();
            ((System.ComponentModel.ISupportInitialize)(this.dgvInventaire)).BeginInit();
            this.gbxFilters.SuspendLayout();
            this.pnlLeft.SuspendLayout();
            this.SuspendLayout();
            // 
            // dgvInventaire
            // 
            this.dgvInventaire.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            this.dgvInventaire.Columns.AddRange(new System.Windows.Forms.DataGridViewColumn[] {
            this.Category,
            this.Code,
            this.Description,
            this.QuantityinHand,
            this.QuantityRes,
            this.QuantityOrder,
            this.QuantityMinimal,
            this.UOM,
            this.Fournisseur,
            this.QuantityEco,
            this.Delays,
            this.Price,
            this.Moyenne,
            this.QuantityProductEst,
            this.Cost});
            this.dgvInventaire.Location = new System.Drawing.Point(205, 193);
            this.dgvInventaire.Name = "dgvInventaire";
            this.dgvInventaire.Size = new System.Drawing.Size(1225, 644);
            this.dgvInventaire.TabIndex = 0;
            // 
            // gbxFilters
            // 
            this.gbxFilters.Controls.Add(this.lblRecherche);
            this.gbxFilters.Controls.Add(this.comboBox2);
            this.gbxFilters.Controls.Add(this.lblFiltre);
            this.gbxFilters.Controls.Add(this.comboBox1);
            this.gbxFilters.Location = new System.Drawing.Point(160, 87);
            this.gbxFilters.Name = "gbxFilters";
            this.gbxFilters.Size = new System.Drawing.Size(1270, 90);
            this.gbxFilters.TabIndex = 1;
            this.gbxFilters.TabStop = false;
            this.gbxFilters.Text = "Filter";
            // 
            // comboBox1
            // 
            this.comboBox1.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.comboBox1.FormattingEnabled = true;
            this.comboBox1.Items.AddRange(new object[] {
            "Catégorie",
            "Fournisseur"});
            this.comboBox1.Location = new System.Drawing.Point(1083, 19);
            this.comboBox1.Name = "comboBox1";
            this.comboBox1.Size = new System.Drawing.Size(181, 24);
            this.comboBox1.TabIndex = 0;
            // 
            // lblFiltre
            // 
            this.lblFiltre.AutoSize = true;
            this.lblFiltre.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.75F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.lblFiltre.ForeColor = System.Drawing.SystemColors.ButtonHighlight;
            this.lblFiltre.Location = new System.Drawing.Point(1031, 22);
            this.lblFiltre.Name = "lblFiltre";
            this.lblFiltre.Size = new System.Drawing.Size(46, 16);
            this.lblFiltre.TabIndex = 1;
            this.lblFiltre.Text = "Filtre:";
            // 
            // lblRecherche
            // 
            this.lblRecherche.AutoSize = true;
            this.lblRecherche.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.75F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.lblRecherche.ForeColor = System.Drawing.SystemColors.ButtonHighlight;
            this.lblRecherche.Location = new System.Drawing.Point(991, 52);
            this.lblRecherche.Name = "lblRecherche";
            this.lblRecherche.Size = new System.Drawing.Size(86, 16);
            this.lblRecherche.TabIndex = 3;
            this.lblRecherche.Text = "Recherche:";
            // 
            // comboBox2
            // 
            this.comboBox2.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.comboBox2.FormattingEnabled = true;
            this.comboBox2.Location = new System.Drawing.Point(1083, 49);
            this.comboBox2.Name = "comboBox2";
            this.comboBox2.Size = new System.Drawing.Size(181, 24);
            this.comboBox2.TabIndex = 2;
            // 
            // pnlLeft
            // 
            this.pnlLeft.Controls.Add(this.btnLocalisation);
            this.pnlLeft.Controls.Add(this.btnPrevisions);
            this.pnlLeft.Controls.Add(this.btnCommandes);
            this.pnlLeft.Controls.Add(this.btnCategories);
            this.pnlLeft.Controls.Add(this.btnFournisseurs);
            this.pnlLeft.Controls.Add(this.btnInventaire);
            this.pnlLeft.Location = new System.Drawing.Point(-2, 4);
            this.pnlLeft.Name = "pnlLeft";
            this.pnlLeft.Size = new System.Drawing.Size(156, 877);
            this.pnlLeft.TabIndex = 2;
            // 
            // btnInventaire
            // 
            this.btnInventaire.BackColor = System.Drawing.SystemColors.AppWorkspace;
            this.btnInventaire.Location = new System.Drawing.Point(3, 50);
            this.btnInventaire.Name = "btnInventaire";
            this.btnInventaire.Size = new System.Drawing.Size(150, 50);
            this.btnInventaire.TabIndex = 0;
            this.btnInventaire.Text = "Liste d\'inventaire";
            this.btnInventaire.UseVisualStyleBackColor = false;
            // 
            // btnFournisseurs
            // 
            this.btnFournisseurs.BackColor = System.Drawing.SystemColors.AppWorkspace;
            this.btnFournisseurs.Location = new System.Drawing.Point(3, 118);
            this.btnFournisseurs.Name = "btnFournisseurs";
            this.btnFournisseurs.Size = new System.Drawing.Size(150, 50);
            this.btnFournisseurs.TabIndex = 1;
            this.btnFournisseurs.Text = "Liste des fournisseurs";
            this.btnFournisseurs.UseVisualStyleBackColor = false;
            // 
            // btnCategories
            // 
            this.btnCategories.BackColor = System.Drawing.SystemColors.AppWorkspace;
            this.btnCategories.Location = new System.Drawing.Point(3, 189);
            this.btnCategories.Name = "btnCategories";
            this.btnCategories.Size = new System.Drawing.Size(150, 50);
            this.btnCategories.TabIndex = 2;
            this.btnCategories.Text = "Liste des catégories";
            this.btnCategories.UseVisualStyleBackColor = false;
            // 
            // btnCommandes
            // 
            this.btnCommandes.BackColor = System.Drawing.SystemColors.AppWorkspace;
            this.btnCommandes.Location = new System.Drawing.Point(3, 262);
            this.btnCommandes.Name = "btnCommandes";
            this.btnCommandes.Size = new System.Drawing.Size(150, 50);
            this.btnCommandes.TabIndex = 3;
            this.btnCommandes.Text = "Liste des commandes";
            this.btnCommandes.UseVisualStyleBackColor = false;
            // 
            // btnPrevisions
            // 
            this.btnPrevisions.BackColor = System.Drawing.SystemColors.AppWorkspace;
            this.btnPrevisions.Location = new System.Drawing.Point(3, 338);
            this.btnPrevisions.Name = "btnPrevisions";
            this.btnPrevisions.Size = new System.Drawing.Size(150, 50);
            this.btnPrevisions.TabIndex = 4;
            this.btnPrevisions.Text = "Commandes et Réceptions";
            this.btnPrevisions.UseVisualStyleBackColor = false;
            // 
            // btnLocalisation
            // 
            this.btnLocalisation.BackColor = System.Drawing.SystemColors.AppWorkspace;
            this.btnLocalisation.Location = new System.Drawing.Point(3, 420);
            this.btnLocalisation.Name = "btnLocalisation";
            this.btnLocalisation.Size = new System.Drawing.Size(150, 50);
            this.btnLocalisation.TabIndex = 5;
            this.btnLocalisation.Text = "Liste des zones";
            this.btnLocalisation.UseVisualStyleBackColor = false;
            // 
            // btnAjouter
            // 
            this.btnAjouter.Location = new System.Drawing.Point(1436, 193);
            this.btnAjouter.Name = "btnAjouter";
            this.btnAjouter.Size = new System.Drawing.Size(143, 50);
            this.btnAjouter.TabIndex = 3;
            this.btnAjouter.Text = "Ajouter";
            this.btnAjouter.UseVisualStyleBackColor = true;
            // 
            // btnSupprimer
            // 
            this.btnSupprimer.Location = new System.Drawing.Point(1436, 249);
            this.btnSupprimer.Name = "btnSupprimer";
            this.btnSupprimer.Size = new System.Drawing.Size(143, 50);
            this.btnSupprimer.TabIndex = 4;
            this.btnSupprimer.Text = "Supprimer";
            this.btnSupprimer.UseVisualStyleBackColor = true;
            // 
            // btnModifier
            // 
            this.btnModifier.Location = new System.Drawing.Point(1436, 305);
            this.btnModifier.Name = "btnModifier";
            this.btnModifier.Size = new System.Drawing.Size(143, 50);
            this.btnModifier.TabIndex = 5;
            this.btnModifier.Text = "Modifier";
            this.btnModifier.UseVisualStyleBackColor = true;
            // 
            // btnImprimer
            // 
            this.btnImprimer.Location = new System.Drawing.Point(1436, 361);
            this.btnImprimer.Name = "btnImprimer";
            this.btnImprimer.Size = new System.Drawing.Size(143, 50);
            this.btnImprimer.TabIndex = 6;
            this.btnImprimer.Text = "Imprimer";
            this.btnImprimer.UseVisualStyleBackColor = true;
            // 
            // btnComm
            // 
            this.btnComm.Location = new System.Drawing.Point(1436, 417);
            this.btnComm.Name = "btnComm";
            this.btnComm.Size = new System.Drawing.Size(143, 50);
            this.btnComm.TabIndex = 7;
            this.btnComm.Text = "Liste des commandes";
            this.btnComm.UseVisualStyleBackColor = true;
            // 
            // btnRes
            // 
            this.btnRes.Location = new System.Drawing.Point(1436, 473);
            this.btnRes.Name = "btnRes";
            this.btnRes.Size = new System.Drawing.Size(143, 50);
            this.btnRes.TabIndex = 8;
            this.btnRes.Text = "Liste des réservations";
            this.btnRes.UseVisualStyleBackColor = true;
            // 
            // btnPrev
            // 
            this.btnPrev.Location = new System.Drawing.Point(1436, 529);
            this.btnPrev.Name = "btnPrev";
            this.btnPrev.Size = new System.Drawing.Size(143, 50);
            this.btnPrev.TabIndex = 9;
            this.btnPrev.Text = "Prévisions de l\'inventaire";
            this.btnPrev.UseVisualStyleBackColor = true;
            // 
            // cbxValeur
            // 
            this.cbxValeur.AutoSize = true;
            this.cbxValeur.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.cbxValeur.ForeColor = System.Drawing.SystemColors.ButtonHighlight;
            this.cbxValeur.Location = new System.Drawing.Point(182, 851);
            this.cbxValeur.Name = "cbxValeur";
            this.cbxValeur.Size = new System.Drawing.Size(194, 20);
            this.cbxValeur.TabIndex = 10;
            this.cbxValeur.Text = "Afficher la valeur des pièces";
            this.cbxValeur.UseVisualStyleBackColor = true;
            // 
            // lblPieces
            // 
            this.lblPieces.AutoSize = true;
            this.lblPieces.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.lblPieces.ForeColor = System.Drawing.SystemColors.ButtonHighlight;
            this.lblPieces.Location = new System.Drawing.Point(1198, 851);
            this.lblPieces.Name = "lblPieces";
            this.lblPieces.Size = new System.Drawing.Size(122, 16);
            this.lblPieces.TabIndex = 11;
            this.lblPieces.Text = "Nombre de pièces:";
            // 
            // tbxPieces
            // 
            this.tbxPieces.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.tbxPieces.Location = new System.Drawing.Point(1324, 848);
            this.tbxPieces.Name = "tbxPieces";
            this.tbxPieces.Size = new System.Drawing.Size(100, 22);
            this.tbxPieces.TabIndex = 12;
            // 
            // Category
            // 
            this.Category.HeaderText = "Catégories";
            this.Category.Name = "Category";
            // 
            // Code
            // 
            this.Code.HeaderText = "Code";
            this.Code.Name = "Code";
            // 
            // Description
            // 
            this.Description.HeaderText = "Description";
            this.Description.Name = "Description";
            // 
            // QuantityinHand
            // 
            this.QuantityinHand.HeaderText = "Qte en main";
            this.QuantityinHand.Name = "QuantityinHand";
            // 
            // QuantityRes
            // 
            this.QuantityRes.HeaderText = "Qte réservée";
            this.QuantityRes.Name = "QuantityRes";
            // 
            // QuantityOrder
            // 
            this.QuantityOrder.HeaderText = "Qte commandée";
            this.QuantityOrder.Name = "QuantityOrder";
            // 
            // QuantityMinimal
            // 
            this.QuantityMinimal.HeaderText = "Qte minimale";
            this.QuantityMinimal.Name = "QuantityMinimal";
            // 
            // UOM
            // 
            this.UOM.HeaderText = "Unité de mesure";
            this.UOM.Name = "UOM";
            // 
            // Fournisseur
            // 
            this.Fournisseur.HeaderText = "Fournisseur";
            this.Fournisseur.Name = "Fournisseur";
            // 
            // QuantityEco
            // 
            this.QuantityEco.HeaderText = "Qte économique";
            this.QuantityEco.Name = "QuantityEco";
            // 
            // Delays
            // 
            this.Delays.HeaderText = "Délai de commande";
            this.Delays.Name = "Delays";
            // 
            // Price
            // 
            this.Price.HeaderText = "Prix unitaire";
            this.Price.Name = "Price";
            // 
            // Moyenne
            // 
            this.Moyenne.HeaderText = "Moyenne / Produit";
            this.Moyenne.Name = "Moyenne";
            // 
            // QuantityProductEst
            // 
            this.QuantityProductEst.HeaderText = "Qte Produit Estimé";
            this.QuantityProductEst.Name = "QuantityProductEst";
            // 
            // Cost
            // 
            this.Cost.HeaderText = "Coût unitaire";
            this.Cost.Name = "Cost";
            // 
            // frmMain
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.BackColor = System.Drawing.SystemColors.ActiveCaption;
            this.ClientSize = new System.Drawing.Size(1584, 880);
            this.Controls.Add(this.tbxPieces);
            this.Controls.Add(this.lblPieces);
            this.Controls.Add(this.cbxValeur);
            this.Controls.Add(this.btnPrev);
            this.Controls.Add(this.btnRes);
            this.Controls.Add(this.btnComm);
            this.Controls.Add(this.btnImprimer);
            this.Controls.Add(this.btnModifier);
            this.Controls.Add(this.btnSupprimer);
            this.Controls.Add(this.btnAjouter);
            this.Controls.Add(this.pnlLeft);
            this.Controls.Add(this.gbxFilters);
            this.Controls.Add(this.dgvInventaire);
            this.Name = "frmMain";
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen;
            this.Text = "Logiciel d\'inventaire";
            ((System.ComponentModel.ISupportInitialize)(this.dgvInventaire)).EndInit();
            this.gbxFilters.ResumeLayout(false);
            this.gbxFilters.PerformLayout();
            this.pnlLeft.ResumeLayout(false);
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.DataGridView dgvInventaire;
        private System.Windows.Forms.GroupBox gbxFilters;
        private System.Windows.Forms.ComboBox comboBox1;
        private System.Windows.Forms.Label lblRecherche;
        private System.Windows.Forms.ComboBox comboBox2;
        private System.Windows.Forms.Label lblFiltre;
        private System.Windows.Forms.Panel pnlLeft;
        private System.Windows.Forms.Button btnInventaire;
        private System.Windows.Forms.Button btnPrevisions;
        private System.Windows.Forms.Button btnCommandes;
        private System.Windows.Forms.Button btnCategories;
        private System.Windows.Forms.Button btnFournisseurs;
        private System.Windows.Forms.Button btnLocalisation;
        private System.Windows.Forms.Button btnAjouter;
        private System.Windows.Forms.Button btnSupprimer;
        private System.Windows.Forms.Button btnModifier;
        private System.Windows.Forms.Button btnImprimer;
        private System.Windows.Forms.Button btnComm;
        private System.Windows.Forms.Button btnRes;
        private System.Windows.Forms.Button btnPrev;
        private System.Windows.Forms.CheckBox cbxValeur;
        private System.Windows.Forms.Label lblPieces;
        private System.Windows.Forms.TextBox tbxPieces;
        private System.Windows.Forms.DataGridViewTextBoxColumn Category;
        private System.Windows.Forms.DataGridViewTextBoxColumn Code;
        private System.Windows.Forms.DataGridViewTextBoxColumn Description;
        private System.Windows.Forms.DataGridViewTextBoxColumn QuantityinHand;
        private System.Windows.Forms.DataGridViewTextBoxColumn QuantityRes;
        private System.Windows.Forms.DataGridViewTextBoxColumn QuantityOrder;
        private System.Windows.Forms.DataGridViewTextBoxColumn QuantityMinimal;
        private System.Windows.Forms.DataGridViewTextBoxColumn UOM;
        private System.Windows.Forms.DataGridViewTextBoxColumn Fournisseur;
        private System.Windows.Forms.DataGridViewTextBoxColumn QuantityEco;
        private System.Windows.Forms.DataGridViewTextBoxColumn Delays;
        private System.Windows.Forms.DataGridViewTextBoxColumn Price;
        private System.Windows.Forms.DataGridViewTextBoxColumn Moyenne;
        private System.Windows.Forms.DataGridViewTextBoxColumn QuantityProductEst;
        private System.Windows.Forms.DataGridViewTextBoxColumn Cost;
    }
}

