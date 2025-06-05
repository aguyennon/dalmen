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
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void btnOptimize_Click(object sender, EventArgs e)
        {
            // Array to hold cut quantity + cut length values inputted
            List<int> cutQtys = new List<int>();
            List<double> cutLengths = new List<double>();

            try
            {
                // Collect values from tbxCutQTY1 - tbxCutQTY8 and tbxCutLength1 - tbxCutLength8
                for (int i = 1; i <= 8; i++)
                {
                    TextBox qtyBox = (TextBox)this.Controls.Find("tbxCutQTY" + i, true).FirstOrDefault();
                    TextBox lenBox = (TextBox)this.Controls.Find("tbxCutLength" + i, true).FirstOrDefault();

                    if (qtyBox != null && lenBox != null)
                    {
                        if (!string.IsNullOrWhiteSpace(qtyBox.Text) && !string.IsNullOrWhiteSpace(lenBox.Text))
                        {
                            int qty = int.Parse(qtyBox.Text);
                            double len = double.Parse(lenBox.Text);

                            if (qty < 0 || len < 0)
                            {
                                MessageBox.Show("All values must be positive.");
                                return;
                            }

                            cutQtys.Add(qty);
                            cutLengths.Add(len);
                        }
                    }
                }

                if (cutQtys.Count == 0)
                {
                    MessageBox.Show("Please enter at least one cut quantity and length.");
                    return;
                }
            }
            catch (FormatException)
            {
                MessageBox.Show("All inputs must be numeric.");
            }
        }

        private void btnExit_Click(object sender, EventArgs e)
        {
            Application.Exit();
        }

        private void Form1_Load(object sender, EventArgs e)
        {

        }
    }
}
