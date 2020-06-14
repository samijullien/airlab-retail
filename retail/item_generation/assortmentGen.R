#Get parameters from console
args  <- commandArgs(trailingOnly = TRUE)
NUMBER_OF_ITEMS <- as.numeric(args[1])
seed <- as.numeric(args[2]) # Generates NA if seed is 'None'.
path <- args[3]
#Load model
library(copula)
load(paste0(path,'/item_generation/copulaModel.RData'))
#Generate data frame with proper column names
itemDesc <-c("Length", "Depth", "Height", "Shelf_life", "Base_Demand", "Cost", "Price")
if(!is.na(seed)){
  set.seed(seed)}
items <- as.data.frame(rMvdc(NUMBER_OF_ITEMS, assortmentCopula))
names(items) <- itemDesc
#ROund shelf life to obtain at least 1 for every item
items$Shelf_life <- ceiling(items$Shelf_life)
write.csv(items, paste0(path,"/item_generation/assortment.csv"))





