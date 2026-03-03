using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DalmenOrders

#region GettersAndSetters
{
    // A whole bunch of getters and setters for the cut items and optimization results
    public class CutItem
    {
        public int Quantity { get; set; }
        public double Length { get; set; }
        public bool IsGroupCut { get; set; } // Indicates if this cut is part of a group cut
        public int OriginalQuantity { get; set; } // Original quantity before grouping
    }
    // For this one, a simple class was used to represent the usage of stock in the optimization process.
    public class StockUsage
    {
        public int BoardNumber { get; set; }
        public double StockLength { get; set; }
        public double CutLength { get; set; }
        public bool IsWaste { get; set; }
    }
    // For this one, a class was created to represent the result of the optimization process
    public class OptimizationResult
    {
        public bool IsSuccess { get; set; }
        public string ErrorMsg { get; set; }
        public int TotalBoards { get; set; }
        public double TotalWaste { get; set; } // Possibly try to reuse some of the waste in future cuts
        public List<StockUsage> Usage { get; set; } = new List<StockUsage>();
    }
}
#endregion
