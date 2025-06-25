using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DalmenOrders
{
    public class CutItem
    {
        public int Quantity { get; set; }
        public double Length { get; set; }
    }

    public class StockUsage
    {
        public int BoardNumber { get; set; }
        public double StockLength { get; set; }
        public double CutLength { get; set; }
        public bool IsWaste { get; set; }
    }

    public class OptimizationResult
    {
        public bool IsSuccess { get; set; }
        public string ErrorMsg { get; set; }
        public int TotalBoards { get; set; }
        public double TotalWaste { get; set; }
        public List<StockUsage> Usage { get; set; } = new List<StockUsage>();
    }
}
