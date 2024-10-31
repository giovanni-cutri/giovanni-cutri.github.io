# importazione dataset ----

cereali <- read.csv("cereal.csv", header = T, sep = ",", dec = ".")

dim(cereali)
str(cereali)

save.image(file = "workspace.RData")

# trasformazione in variabili categoriche ----

cereali$shelf <- factor(cereali$shelf, labels = c("First", "Second", "Third"), 
                        ordered = T)

cereali$mfr <- factor(cereali$mfr)
cereali$type <- factor(cereali$type)

str(cereali$shelf)
str(cereali$mfr)
str(cereali$type)

# analisi variabile "mfr" ----

table(cereali$mfr)

percentuali <- round(prop.table(table(cereali$mfr))*100, digits = 2)
etichette <- paste(names(percentuali), percentuali)
etichette <- paste(etichette, "%", sep = "")

pie(table(cereali$mfr), main = "Grafico a torta per i produttori", col=1:7,
    labels = etichette)

barplot(table(cereali$mfr), main = "Grafico a barre per i produttori",
        names.arg = names(table(cereali$mfr)), col = "burlywood")


# analisi variabile "type" ----

table(cereali$type)

percentuali <- round(prop.table(table(cereali$type))*100, digits = 2)
etichette <- paste(names(percentuali), percentuali)
etichette <- paste(etichette, "%", sep = "")

pie(table(cereali$type), main = "Grafico a torta per la tipologia di cereali", 
    col = c("blue", "red"), labels = etichette)


# analisi variabile "calories" ----

summary(cereali$calories)
IQR(cereali$calories)
var(cereali$calories)
sd(cereali$calories)

boxplot(cereali$calories, main = "Distribuzione delle calorie")

hist(cereali$calories, main = "Distribuzione delle calorie", probability = TRUE,
     xlab = "Calorie", col = "darkblue")


# analisi variabili nutrienti ----

summary(cereali$protein)
summary(cereali$fat)
summary(cereali$sodium)
summary(cereali$fiber)
summary(cereali$carbo)
summary(cereali$sugars)
summary(cereali$potass)

cereali$carbo[cereali$carbo<0] <- median(cereali$carbo)
cereali$sugars[cereali$sugars<0] <- median(cereali$sugars)
cereali$potass[cereali$potass<0] <- median(cereali$potass)

boxplot(cereali$protein, main = "Distribuzione delle proteine")
boxplot(cereali$fat, main = "Distribuzione dei grassi")
boxplot(cereali$sodium, main = "Distribuzione del sodio")
boxplot(cereali$fiber, main = "Distribuzione delle fibre")
boxplot(cereali$carbo, main = "Distribuzione dei carboidrati")
boxplot(cereali$sugars, main = "Distribuzione degli zuccheri")
boxplot(cereali$potass, main = "Distribuzione del potassio")


# conversione variabile numerica in categorica ----

summary(cereali$rating)
rating.categorica <- cut(cereali$rating, breaks = c(0,40,60,100), right = F)
rating.categorica <- factor(rating.categorica, labels = c("cattivo", "mediocre",
                                                          "buono"), ordered=T)
table(rating.categorica)


# connessione tra produttori e rating ----

table(cereali$mfr, rating.categorica)

chisq.test(table(cereali$mfr, rating.categorica))
X.squared <- chisq.test(table(cereali$mfr, rating.categorica))
X.squared$statistic

phi <- as.numeric(X.squared$statistic) / nrow(cereali)
Tschuprow <- sqrt(phi/sqrt(12))
Tschuprow


# dipendenza in media calorie e rating ----

hist(cereali$calories[rating.categorica == "cattivo"], xlim = c(50,160),
     col = 2, main = "Distribuzione calorie in base al rating", xlab = "Calorie", 
     probability=T)

hist(cereali$calories[rating.categorica == "mediocre"], xlim = c(50,160), 
     col = 7, add = T, probability=T)

hist(cereali$calories[rating.categorica == "buono"], xlim = c(50,160), col = 3, 
     add=T, probability=T)

legend (x="topright", title="Rating", legend=levels(rating.categorica), 
        col = c(2,7,3), fill = c(2,7,3))


boxplot(cereali$calories~rating.categorica, xlab = "Rating", ylab = "Calorie")

tapply(cereali$calories, rating.categorica, summary)

aov.cal <- summary(aov(cereali$calories~rating.categorica))
dev <- aov.cal[[1]]$`Sum Sq` 
eta.squared <- dev[1] / sum(dev)
eta.squared


# dipendenza lineare tra due nutrienti ----

cereali.num <- cereali

cereali.num$name <- NULL
cereali.num$mfr <- NULL
cereali.num$type <- NULL
cereali.num$calories <- NULL
cereali.num$shelf <- NULL
cereali.num$weight <- NULL
cereali.num$cups <- NULL
cereali.num$rating <- NULL

cereali.mat <- as.matrix(cereali.num)

round(cor(cereali.mat), 4)

cor(cereali$fiber, cereali$potass)
plot(cereali$fiber, cereali$potass, main = "Relazione tra potassio e fibre", 
     xlab = "Fibre", ylab = "Potassio")
reg.potass <- lm(cereali$potass~cereali$fiber)
summary(reg.potass)
abline(reg.potass, col = "green")

cor(cereali$protein, cereali$sugars)
plot(cereali$protein, cereali$sugars, main = "Relazione tra zuccheri e proteine",
     xlab = "Proteine", ylab = "Zuccheri")
reg.sugars <- lm(cereali$sugars~cereali$protein)
summary(reg.sugars)
abline(reg.sugars, col = "green")