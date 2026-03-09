using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace DiagonalCutOptimizer
{

    public partial class frmMain : Form
    {
        private const int INITIAL_RULER_POSITION = 3300;
        private const int SAW_DISTANCE = 900;
        private const int MIN_RULER_POSITION = 854;


        public frmMain()
        {
            InitializeComponent();
        }

        private void frmMain_Load(object sender, EventArgs e)
        {
            InitializeRadOnlyFields();
        }
        private void InitializeRadOnlyFields()
        {
            var editableFields = new[]
            {
            txtStock, txtRequired,
            txtRequired1, txtRequired2, txtRequired3,
            txtRequired4, txtRequired5, txtRequired6
        };

            foreach (Control control in this.Controls)
            {
                if (control is TextBox textBox && !editableFields.Contains(textBox))
                {
                    textBox.ReadOnly = true;
                    textBox.BackColor = SystemColors.Control;
                }
            }

            SetReadOnlyRecursive(this, editableFields);
        }

        private void SetReadOnlyRecursive(Control parent, TextBox[] editableFields)
        {
            foreach (Control control in parent.Controls)
            {
                if (control is TextBox textBox && !editableFields.Contains(textBox))
                {
                    textBox.ReadOnly = true;
                    textBox.BackColor = SystemColors.Control;
                }
                else if (control.HasChildren)
                {
                    SetReadOnlyRecursive(control, editableFields);
                }
            }
        }



        private void btnClose_Click(object sender, EventArgs e)
        {
            this.Close();
        }

        private void btnClear_Click(object sender, EventArgs e)
        {
            RemoveExistingWarningLabels();

            txtStock.Text = "";
            txtRequired.Text = "";
            txtStock1.Text = "";
            txtStock2.Text = "";
            txtStock3.Text = "";
            txtStock4.Text = "";
            txtStock5.Text = "";
            txtStock6.Text = "";
            txtStartPos1.Text = "";
            txtStartPos2.Text = "";
            txtStartPos3.Text = "";
            txtStartPos4.Text = "";
            txtStartPos5.Text = "";
            txtStartPos6.Text = "";
            txtRequired1.Text = "";
            txtRequired2.Text = "";
            txtRequired3.Text = "";
            txtRequired4.Text = "";
            txtRequired5.Text = "";
            txtRequired6.Text = "";
            txtMove1.Text = "";
            txtMove2.Text = "";
            txtMove3.Text = "";
            txtMove4.Text = "";
            txtMove5.Text = "";
            txtMove6.Text = "";
            txtRuler1.Text = "";
            txtRuler2.Text = "";
            txtRuler3.Text = "";
            txtRuler4.Text = "";
            txtRuler5.Text = "";
            txtRuler6.Text = "";

        }

        private void btnOptimize_Click(object sender, EventArgs e)
        {
            try
            {
                if (!ValidateInputs())
                    return;

                int stockLength = int.Parse(txtStock.Text);
                int requiredLength = int.Parse(txtRequired.Text);

                CalculateTrims(stockLength, requiredLength);
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Error during optimization: {ex.Message}", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private bool ValidateInputs()
        {
            if (string.IsNullOrWhiteSpace(txtStock.Text) ||
                string.IsNullOrWhiteSpace(txtRequired.Text))
            {
                MessageBox.Show("Please enter both Stock and Required values.",
                          "Missing Input", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                return false;
            }

            if (!int.TryParse(txtStock.Text, out int stock) ||
                !int.TryParse(txtRequired.Text, out int required))
            {
                MessageBox.Show("Please enter valid numeric values.",
                          "Invalid Input", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                return false;
            }

            if (stock <= 0 || required <= 0)
            {
                MessageBox.Show("Values must be greater than 0.",
                              "Invalid Input", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                return false;
            }

            return true;
        }

        private void CalculateTrims(int stockLength, int requiredLength)
        {
            // Clear all trim fields first
            ClearAllTrims();

            var trimData = new[]
            {
        new { StockBox = txtStock1, StartPosBox = txtStartPos1, RequiredBox = txtRequired1,
              DiffBox = txtMove1, RulerBox = txtRuler1 },
        new { StockBox = txtStock2, StartPosBox = txtStartPos2, RequiredBox = txtRequired2,
              DiffBox = txtMove2, RulerBox = txtRuler2 },
        new { StockBox = txtStock3, StartPosBox = txtStartPos3, RequiredBox = txtRequired3,
              DiffBox = txtMove3, RulerBox = txtRuler3 },
        new { StockBox = txtStock4, StartPosBox = txtStartPos4, RequiredBox = txtRequired4,
              DiffBox = txtMove4, RulerBox = txtRuler4 },
        new { StockBox = txtStock5, StartPosBox = txtStartPos5, RequiredBox = txtRequired5,
              DiffBox = txtMove5, RulerBox = txtRuler5 },
        new { StockBox = txtStock6, StartPosBox = txtStartPos6, RequiredBox = txtRequired6,
              DiffBox = txtMove6, RulerBox = txtRuler6 }
    };

            int currentRulerPosition = INITIAL_RULER_POSITION;
            int remainingStock = stockLength;
            int trimCount = 0;
            bool woodBlockWarningShown = false;
            int woodBlockTrimIndex = -1;

            RemoveExistingWarningLabels();

            for (int i = 0; i < trimData.Length; i++)
            {
                var trim = trimData[i];

                int thisRequiredLength = requiredLength;
                if (!string.IsNullOrWhiteSpace(trim.RequiredBox.Text))
                {
                    if (int.TryParse(trim.RequiredBox.Text, out int customRequired) && customRequired > 0)
                        thisRequiredLength = customRequired;
                }
                else
                {
                    trim.RequiredBox.Text = requiredLength.ToString();
                }

                // Check if there's enough stock for this trim
                if (remainingStock < thisRequiredLength)
                {
                    // Clear the required field and show "Not enough stock"
                    trim.RequiredBox.Text = "";
                    continue; // Skip to next trim
                }

                int diffToMove = SAW_DISTANCE - thisRequiredLength;
                int rulerPositionAfterCut = currentRulerPosition + diffToMove;

                if (rulerPositionAfterCut < MIN_RULER_POSITION)
                {
                    currentRulerPosition += 2000;
                    rulerPositionAfterCut = currentRulerPosition + diffToMove;

                    if (!woodBlockWarningShown)
                    {
                        woodBlockTrimIndex = i;
                        woodBlockWarningShown = true;
                    }

                    if (rulerPositionAfterCut < MIN_RULER_POSITION)
                        break;
                }

                trim.StockBox.Text = remainingStock.ToString();
                trim.StartPosBox.Text = currentRulerPosition.ToString();
                trim.DiffBox.Text = diffToMove.ToString();
                trim.RulerBox.Text = rulerPositionAfterCut.ToString();

                remainingStock -= thisRequiredLength;
                currentRulerPosition = rulerPositionAfterCut - SAW_DISTANCE;
                trimCount++;
            }

            if (woodBlockTrimIndex >= 0)
            {
                AddWoodBlockWarning(woodBlockTrimIndex);
            }
        }

        private void AddWoodBlockWarning(int trimIndex)
        {
            GroupBox trimGroupBox = null;
            switch (trimIndex)
            {
                case 0: trimGroupBox = gbxFirst; break;
                case 1: trimGroupBox = gbxSecond; break;
                case 2: trimGroupBox = gbxThird; break;
                case 3: trimGroupBox = gbxFourth; break;
                case 4: trimGroupBox = gbxFifth; break;
                case 5: trimGroupBox = gbxSixth; break;

            }
            if (trimGroupBox != null)
            {
                Label warningLabel = CreateWoodBlockWarningLabel();
                warningLabel.Name = "WoodBlockWarning" + trimIndex;

                warningLabel.Location = new Point(trimGroupBox.Left + 175, trimGroupBox.Top - 5);
                warningLabel.Size = new Size(trimGroupBox.Width - 20, 20); // Set explicit size

                // Add to the same parent container as the groupbox
                trimGroupBox.Parent.Controls.Add(warningLabel);
                warningLabel.BringToFront();
            }
        }

        private void RemoveExistingWarningLabels()
        {
            for (int i = 0; i < 6; i++)
            {
                string labelName = "WoodBlockWarning" + i; 
                Control existingLabel = this.Controls.Find(labelName, true).FirstOrDefault();
                if (existingLabel != null)
                {
                    existingLabel.Parent.Controls.Remove(existingLabel);
                }
            }
        }

        private Label CreateWoodBlockWarningLabel()
        {
            Label warningLabel = new Label();
            warningLabel.Text = "WARNING! WOOD BLOCK NEEDED BELOW : 2000MM";
            warningLabel.ForeColor = Color.Red;
            warningLabel.Font = new Font(warningLabel.Font, FontStyle.Bold);
            warningLabel.AutoSize = true;
            warningLabel.TextAlign = ContentAlignment.MiddleCenter;
            return warningLabel;
        }

        private void ClearAllTrims()
        {
            var allTrimBoxes = new[]
            {
            txtStock1, txtStartPos1, txtMove1, txtRuler1,
            txtStock2, txtStartPos2, txtMove2, txtRuler2,
            txtStock3, txtStartPos3, txtMove3, txtRuler3,
            txtStock4, txtStartPos4, txtMove4, txtRuler4,
            txtStock5, txtStartPos5, txtMove5, txtRuler5,
            txtStock6, txtStartPos6, txtMove6, txtRuler6
        };

            foreach (var textBox in allTrimBoxes)
            {
                textBox.Clear();
            }
        }

        private bool ValidateStockInput()
        {
            if (int.TryParse(txtStock.Text, out int stockValue))
            {
                if (stockValue > 4738)
                {
                    MessageBox.Show("Stock length cannot exceed 4738 mm.",
                        "Stock Length Cap", MessageBoxButtons.OK, MessageBoxIcon.Information);
                    txtStock.Text = "4738";
                    return true;
                }
            }
            return true;
        }

        private void txtStock_TextChanged(object sender, EventArgs e)
        {
            ValidateStockInput();
        }
    }   
    }
