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

    public class CutItemWithDelignage : CutItem
    {
        public string Delignage { get; set; } 
        public int OrderSequence { get; set; } 
    }

    public class DelignageGroup
    {
        public string DelignageValue { get; set; }
        public List<CutItem> Cuts { get; set; } = new List<CutItem>();
        public int TotalPieces { get; set; }
        public double TotalLength { get; set; }
    }
    public class DelignageOptimizationResult
    {
        public string DelignageValue { get; set; }
        public OptimizationResult OptimizationResult { get; set; }
        public List<CutItem> CutsForThisDelignage { get; set; }
    }

    public class MultiDelignageResult
    {
        public List<DelignageOptimizationResult> DelignageResults { get; set; } = new List<DelignageOptimizationResult>();
        public string LotNumber { get; set; }
        public bool HasMultipleDelignage => DelignageResults.Count > 1;
    }

}
