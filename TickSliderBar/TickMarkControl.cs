using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Drawing;
using System.Windows.Forms;

namespace TickSliderBar
{
    public partial class TickMarkControl : UserControl
    {
        private int _selectedValue = 0;
        private int _minValue = -15;
        private int _maxValue = 15;

        public int SelectedValue
        {
            get { return _selectedValue; }
            set
            {
                if (value >= _minValue && value <= _maxValue)
                {
                    _selectedValue = value;
                    Invalidate(); 
                }
            }
        }

        public int MinValue
        {
            get { return _minValue; }
            set { _minValue = value; Invalidate(); }
        }

        public int MaxValue
        {
            get { return _maxValue; }
            set { _maxValue = value; Invalidate(); }
        }

        public TickMarkControl()
        {
            InitializeComponent();
            SetStyle(ControlStyles.AllPaintingInWmPaint |
                     ControlStyles.UserPaint |
                     ControlStyles.DoubleBuffer, true);
            this.Size = new Size(400, 80);
            this.BackColor = Color.White;
        }

        private void InitializeComponent()
        {
            this.SuspendLayout();
            this.Name = "TickMarkControl";
            this.MouseClick += TickMarkControl_MouseClick;
            this.ResumeLayout(false);
        }

        protected override void OnPaint(PaintEventArgs e)
        {
            base.OnPaint(e);
            Graphics g = e.Graphics;
            g.SmoothingMode = System.Drawing.Drawing2D.SmoothingMode.AntiAlias;

            // Calculate dimensions
            int totalTicks = _maxValue - _minValue + 1; // 31 ticks (-15 to 15)
            int margin = 20;
            int availableWidth = this.Width - (2 * margin);
            float tickSpacing = availableWidth / (float)(totalTicks - 1);

            int tickHeight = 10;
            int tickY = this.Height / 2 - tickHeight / 2;
            int numberY = tickY + tickHeight + 5;

            // Draw the horizontal line
            using (Pen linePen = new Pen(Color.Black, 2))
            {
                int lineY = this.Height / 2;
                g.DrawLine(linePen, margin, lineY, this.Width - margin, lineY);
            }

            // Draw tick marks and numbers
            using (Pen tickPen = new Pen(Color.Black, 1))
            using (Font font = new Font("Arial", 8))
            using (Brush textBrush = new SolidBrush(Color.Black))
            {
                for (int i = 0; i < totalTicks; i++)
                {
                    int value = _minValue + i;
                    float x = margin + (i * tickSpacing);

                    // Draw tick mark
                    g.DrawLine(tickPen, x, tickY, x, tickY + tickHeight);

                    // Draw number
                    string text = value.ToString();
                    SizeF textSize = g.MeasureString(text, font);
                    g.DrawString(text, font, textBrush,
                        x - textSize.Width / 2, numberY);
                }
            }

            // Draw the selected value indicator (blue circle)
            if (_selectedValue >= _minValue && _selectedValue <= _maxValue)
            {
                int selectedIndex = _selectedValue - _minValue;
                float selectedX = margin + (selectedIndex * tickSpacing);
                int circleRadius = 8;
                int circleY = this.Height / 2 - circleRadius;

                using (Brush blueBrush = new SolidBrush(Color.Blue))
                {
                    g.FillEllipse(blueBrush,
                        selectedX - circleRadius,
                        circleY,
                        circleRadius * 2,
                        circleRadius * 2);
                }
            }
        }

        private void TickMarkControl_MouseClick(object sender, MouseEventArgs e)
        {
            // Calculate which tick was clicked
            int totalTicks = _maxValue - _minValue + 1;
            int margin = 20;
            int availableWidth = this.Width - (2 * margin);
            float tickSpacing = availableWidth / (float)(totalTicks - 1);

            // Find the closest tick to the mouse position
            float relativeX = e.X - margin;
            int clickedIndex = (int)Math.Round(relativeX / tickSpacing);

            if (clickedIndex >= 0 && clickedIndex < totalTicks)
            {
                SelectedValue = _minValue + clickedIndex;
            }
        }
    }
}
