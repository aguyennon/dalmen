using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace DalmenOrders
{
    internal static class Program
    {
        /// <summary>
        /// The main entry point for the application.
        /// </summary>
        [STAThread]
        static void Main()
        {
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);
            Application.Run(new Form1());

            InputForm inputForm = new InputForm();

            if (inputForm.ShowDialog() == DialogResult.OK)
            {
                Form1 mainForm = new Form1();

                if (inputForm.DataProcessed && inputForm.ProcessedCuts.Count > 0)
                {
                    mainForm.LoadProcessedCuts(inputForm.ProcessedCuts);
                }
                
                Application.Run(mainForm);
            }
        }
    }
}
