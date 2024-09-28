#Check you working directory
getwd()

data <- read.csv("Data_csv/StatsPlayers_2009-2010.csv", header=TRUE, sep = ",")

#Variables
a<-1
# Functions
my.sum <- function(a=2,b=1){
  return(a+b)
}

my.sum(3,4)

#Recursion
fac <- function(n) {
  ifelse(n==1,return(1), return(n*fac(n-1)))
}

#Types
class(my.sum)
class(a)

#Para leer documentación acerca de una función usamos el comando "help" o ?:
help(ls)
?ls
#para un comando particular
help('for')
ls()

#View my workspace environment
objects()
rm(a)
#to delete them all
rm(list=ls())

#We can save all my workspace variables in a file and then retrieve my work in a future season
save.image('~/myworkspace.RData')
#We can load it in a new session
load('myworkspace.RData')

#Vectors

ages<-c(21,33,12,34,23,70,90,80,7,29,14,2,
        88,11,55,24,13,11,56,28,33)

a.sum<-sum(ages)
a.length<-length(ages)
a.sum
a.length

numbers<-c(1,2,3)
numbers+3
numbers*5

#Vectors 2

a.mean<- sum(ages)/length(ages)
a.mean
a.var<-sum((ages-a.mean)^2)/(length(ages)-1)
a.var

#mean and var functions:
mean(ages)
var(ages)
?var

#Cuando construimos vectores con elementos de diferentes tipos, R los convierte todos
#en un sólo tipo de datos:

c("hello",2,T)
c(TRUE,FALSE,500)

#Los elementos de un fector pueden ser declarados con nombres y entonces recuperarlos 
#con sus nombres:

grades<-c(Juan=4.5, Luis=6.2,Romina=3.9,Felipe=2.8,Mariana=6.7)
names(grades)

#Podemos ordenar un vector usango sort:

names(sort(x=grades, decreasing=T))

#Acceso a elementos:
grades[0]
grades[1]
grades[-2]
grades[c(1,5)]
grades[c('Juan','Mariana')]




