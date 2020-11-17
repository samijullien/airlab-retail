from rpy2 import robjects
from rpy2.robjects.packages import importr



def Rscript(size, seed, path):
    """assortmentGen.R script"""
    robjects.r(f'NUMBER_OF_ITEMS <- as.numeric({size})')

    # Load model
    copula = importr("copula")
    robjects.r(f'load(paste0("{path}","/copulaModel.RData"))')

    # Generate data frame with proper column names
    robjects.r('itemDesc <-c("Length", "Depth", "Height", "Shelf_life", "Base_Demand", "Cost", "Price")')
    if seed is not None:
        robjects.r(f'set.seed({seed})')
    robjects.r('items <- as.data.frame(rMvdc(NUMBER_OF_ITEMS, assortmentCopula))')
    robjects.r('names(items) <- itemDesc')

    # Round shelf life to obtain at least 1 for every item
    robjects.r('items$Shelf_life <- ceiling(items$Shelf_life)')
    robjects.r(f'write.csv(items, paste0("{path}","/assortment.csv"))')
