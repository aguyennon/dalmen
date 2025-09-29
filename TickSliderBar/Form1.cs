using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace TickSliderBar
{
    public partial class Form1 : Form
    {
        private TickMarkControl tickMarkControl;
        private Label valueLabel;
        private Timer updateTimer;
        private int lastValue = 0;

        public Form1()
        {
            InitializeComponent(); // This calls the auto-generated method
            SetupCustomControls();  // This calls our custom setup method
        }

        private void SetupCustomControls()
        {
            // Form properties
            this.Text = "Tick Mark for Markel N' Friends!";
            this.Size = new Size(900, 250);
            this.StartPosition = FormStartPosition.CenterScreen;

            // Create the tick mark control
            tickMarkControl = new TickMarkControl();
            tickMarkControl.Location = new Point(50, 50);
            tickMarkControl.Size = new Size(800, 80);
            tickMarkControl.SelectedValue = 0; // Start at center
            this.Controls.Add(tickMarkControl);

            // Create a label to show the selected value
            valueLabel = new Label();
            valueLabel.Text = "SELECTED VALUE: 0";
            valueLabel.Location = new Point(50, 150);
            valueLabel.Size = new Size(200, 20);
            valueLabel.Font = new Font("Arial", 12);
            this.Controls.Add(valueLabel);

            // Set up timer to check for changes
            updateTimer = new Timer();
            updateTimer.Interval = 100;
            updateTimer.Tick += UpdateTimer_Tick;
            updateTimer.Start();
        }

        private void UpdateTimer_Tick(object sender, EventArgs e)
        {
            if (tickMarkControl.SelectedValue != lastValue)
            {
                lastValue = tickMarkControl.SelectedValue;
                valueLabel.Text = $"SELECTED VALUE: {lastValue}";
            }
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            // This method can stay empty or you can add initialization code here
        }
    }
}