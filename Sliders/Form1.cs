using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Sliders
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();

            TrackBar trackBar = new TrackBar();
            trackBar.Minimum = 0;
            trackBar.Maximum = 100;
            trackBar.TickFrequency = 25;
            trackBar.Value = 50;
            trackBar.Location = new Point(297, 300);
            trackBar.Width = 321;
            this.Controls.Add(trackBar);

            // Editable numbers under the TrackBar
            int[] values = { 0, 25, 50, 75, 100 };
            TextBox[] textBoxes = new TextBox[values.Length];

            for (int i = 0; i < values.Length; i++)
            {
                TextBox txt = new TextBox();
                txt.Text = values[i].ToString();
                txt.Width = 40;

                // position under the ticks
                int x = trackBar.Left + (i * (trackBar.Width - 1) / (values.Length - 1)) - txt.Width / 3;
                int y = trackBar.Bottom + 5;

                txt.Location = new Point(x, y);
                textBoxes[i] = txt;
                this.Controls.Add(txt);

                // When user changes text, update values[]
                txt.TextChanged += (s, e) =>
                {
                    int index = Array.IndexOf(textBoxes, txt);
                    if (int.TryParse(txt.Text, out int newVal))
                    {
                        values[index] = newVal;
                        // 👉 You could also do something with trackBar here if needed
                    }
                };
            }
        }
        

        private void Form1_Load(object sender, EventArgs e)
        {

        }
    }
}
