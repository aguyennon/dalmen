using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Data.SqlClient;
using System.Drawing;
using System.Linq;
using System.Runtime.CompilerServices;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace ThermosProject
{
    public partial class frmMain : Form
    {

        string connStringSQL = "Data Source=DSI01DATA01;Initial Catalog=Verres_Dalumex;User ID=SuiviProd;Password=SuiviProd;";
        public frmMain()
        {
            InitializeComponent();
        }

        private void btnLoad_Click(object sender, EventArgs e)
        {
            for (int i = 1; i <= 15; i++)
            {
                TextBox tbxCode = this.Controls.Find($"tbxCode{i}", true).FirstOrDefault() as TextBox;
                if (tbxCode == null || string.IsNullOrWhiteSpace(tbxCode.Text))
                    continue;

                string barcode = tbxCode.Text.Trim();
                DataRow result = GetBarcodeData(barcode);

                if (result != null)
                {
                    (this.Controls.Find($"tbxLot{i}", true).FirstOrDefault() as TextBox).Text = result["strLotUsine"].ToString();
                    (this.Controls.Find($"tbxDim{i}", true).FirstOrDefault() as TextBox).Text = result["strDimension"].ToString();
                    (this.Controls.Find($"tbxDesc{i}", true).FirstOrDefault() as TextBox).Text = result["strDescription"].ToString();
                    (this.Controls.Find($"tbxFini{i}", true).FirstOrDefault() as TextBox).Text = result["strFini"].ToString();
                    (this.Controls.Find($"tbxLarg{i}", true).FirstOrDefault() as TextBox).Text = result["dblLargeur"].ToString();
                    (this.Controls.Find($"tbxHaut{i}", true).FirstOrDefault() as TextBox).Text = result["dblHauteur"].ToString();
                    (this.Controls.Find($"tbxVerre{i}", true).FirstOrDefault() as TextBox).Text = result["strEpais"].ToString();
                    (this.Controls.Find($"tbxChaine{i}", true).FirstOrDefault() as TextBox).Text = result["strLigne"].ToString();
                    (this.Controls.Find($"tbxDalumex{i}", true).FirstOrDefault() as TextBox).Text = result["strFichierProd"].ToString();
                    (this.Controls.Find($"tbxDate{i}", true).FirstOrDefault() as TextBox).Text = result["datDateFait"].ToString(); 

                }
            }
        }

        private DataRow GetBarcodeData(string barcode)
        {
            DataTable dt = QueryDatabase(connStringSQL, barcode);
            if (dt.Rows.Count == 0)
                dt = QueryDatabase(connStringSQL, barcode);

            return dt.Rows.Count > 0 ? dt.Rows[0] : null;

        }

        private DataTable QueryDatabase(string connString, string barcode)
        {
            DataTable dt = new DataTable();

            string query = @"
        SELECT 
            [strCodeBarre],
            [strLotUsine],
            [strDimension],
            [strDescription],
            [strFini],
            [dblLargeur],
            [dblHauteur],
            [strEpais],
            [strLigne],
            [strFichierProd],
            [datDateFait]
        FROM [Verres_Dalumex].[dbo].[viewVerres]
        WHERE [strCodeBarre] = @barcode";

            using (SqlConnection conn = new SqlConnection(connString))
            using (SqlCommand cmd = new SqlCommand(query, conn))
            using (SqlDataAdapter da = new SqlDataAdapter(cmd))
            {
                cmd.Parameters.AddWithValue("@barcode", barcode);
                da.Fill(dt);
            }

            return dt;
        }

        private void btnClearCodes_Click(object sender, EventArgs e)
        {
            tbxCode1.Clear();
            tbxCode2.Clear();
            tbxCode3.Clear();
            tbxCode4.Clear();
            tbxCode5.Clear();
            tbxCode6.Clear();
            tbxCode7.Clear();
            tbxCode8.Clear();
            tbxCode9.Clear();
            tbxCode10.Clear();
            tbxCode11.Clear();
            tbxCode12.Clear();
            tbxCode13.Clear();
            tbxCode14.Clear();
            tbxCode15.Clear();
        }

        private void ClearTextBoxes(Control parent)
        {
            foreach (Control c in parent.Controls)
            {
                if (c is TextBox textBox && textBox.Name != "tbxCode1" && textBox.Name != "tbxCode2" && textBox.Name != "tbxCode3" &&
                    textBox.Name != "tbxCode4" && textBox.Name != "tbxCode5" && textBox.Name != "tbxCode6" &&
                    textBox.Name != "tbxCode7" && textBox.Name != "tbxCode8" && textBox.Name != "tbxCode9" &&
                    textBox.Name != "tbxCode10" && textBox.Name != "tbxCode11" && textBox.Name != "tbxCode12" &&
                    textBox.Name != "tbxCode13" && textBox.Name != "tbxCode14" && textBox.Name != "tbxCode15")
                {
                    textBox.Clear();
                }
                else if (c.HasChildren)
                {
                    ClearTextBoxes(c);
                }
            }
        }

        private void btnClearResults_Click(object sender, EventArgs e)
        {
            ClearTextBoxes(this);
        }

        private void btnExit_Click(object sender, EventArgs e)
        {
            Application.Exit();
        }

        private void btnForm2_Click(object sender, EventArgs e)
        {
            frmSecond secondForm = new frmSecond(this); 
            secondForm.Show();
        }

        private void frmMain_Load(object sender, EventArgs e)
        {

        }
    }
}
