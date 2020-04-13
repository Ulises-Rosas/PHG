library(ggplot2)
library(dplyr)
library(vegan)


df_barplot  = read.csv("project/taxa_abund-2.csv", stringsAsFactors = F )

tmp_df = as.data.frame(t(df_barplot), stringsAsFactors = F)
colnames(tmp_df) <- as.character(tmp_df[1,])
df = tmp_df[-1,]

df[, !grepl("(region|sample)", colnames(df))] %>%
  dplyr::mutate_all(as.numeric)  %>%
  colSums(x = .) %>%
  sort(x = .) %>%
  names(x = .) -> taxaorder



do.call(
  "rbind",
  lapply(
    unique(df$region),
    function(x){
      tmp    = df[grepl(x, df$region),]
      counts = tmp[,!grepl("(region|sample)", colnames(tmp))]
      
      do.call(
        "rbind",
        lapply(
          row.names(counts),
          function(y){
            
            subcounts = counts[y,]
            subcounts = subcounts[as.numeric(subcounts) > 0]
            taxanames = names(subcounts)
            nvalue    = as.numeric(subcounts)
            prop      = nvalue/sum(nvalue)
            taxanames = factor(taxanames,levels = rev(taxaorder),ordered = T)
            
            data.frame(
              region = x,
              samples = y,
              taxa = taxanames,
              n    = prop
              # ,stringsAsFactors = F
            )
          })
        ) -> subdf
    
      indexer        <- subdf$n
      names(indexer) <- subdf$samples
      
      dd <- vegan::vegdist(indexer, method = "bray" )
      hc <- hclust(dd, method = "ward.D2")
    
      # attributes(hc)
      subdf <- subdf[hc$order,]
      subdf$samples <- as.factor(subdf$samples)
      subdf
    })
) -> maintoplotbar

# maintoplotbar$taxa
jpeg("baplots_microbiomes.jpeg", width = 69.26, height = 15.8, units = 'in', res = 200)
ggplot(data = maintoplotbar, aes(y = n, x = samples, fill = taxa)) +
  geom_bar(stat =  "identity") +
  scale_fill_brewer(palette = "Set3") +
  facet_wrap(~region,  scales = "free_x", nrow = 1) +
  theme_bw(base_size = 64) + 
  theme(legend.position="bottom",
        axis.text.x=element_blank(),
        axis.ticks.x=element_blank()) 
dev.off()
