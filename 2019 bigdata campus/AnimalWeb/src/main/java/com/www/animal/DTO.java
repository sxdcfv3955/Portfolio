package com.www.animal;

import java.io.Serializable;

public class DTO implements Serializable{
   private int kindDog;
   private int kindEtc;
   private double ageN;
   private double weightN;
   private int neuterN;
   private int sggGu;
   private int sggSi;
   
   
   public DTO(double ageN, double weightN, int neuterN, int sggGu, int sggSi) {
      super();
      this.ageN = ageN;
      this.weightN = weightN;
      this.neuterN = neuterN;
      this.sggGu = sggGu;
      this.sggSi = sggSi;
   }
   
   
   public DTO(int kindDog, int kindEtc, double ageN, double weightN, int neuterN, int sggGu, int sggSi) {
      super();
      this.kindDog = kindDog;
      this.kindEtc = kindEtc;
      this.ageN = ageN;
      this.weightN = weightN;
      this.neuterN = neuterN;
      this.sggGu = sggGu;
      this.sggSi = sggSi;
   }

   public int getKindDog() {
      return kindDog;
   }

   public void setKindDog(int kindDog) {
      this.kindDog = kindDog;
   }

   public int getKindEtc() {
      return kindEtc;
   }

   public void setKindEtc(int kindEtc) {
      this.kindEtc = kindEtc;
   }

   public double getAgeN() {
      return ageN;
   }

   public void setAgeN(double ageN) {
      this.ageN = ageN;
   }

   public double getWeightN() {
      return weightN;
   }

   public void setWeightN(double weightN) {
      this.weightN = weightN;
   }

   public int getNeuterN() {
      return neuterN;
   }

   public void setNeuterN(int neuterN) {
      this.neuterN = neuterN;
   }

   public int getSggGu() {
      return sggGu;
   }

   public void setSggGu(int sggGu) {
      this.sggGu = sggGu;
   }

   public int getSggSi() {
      return sggSi;
   }

   public void setSggSi(int sggSi) {
      this.sggSi = sggSi;
   }

   @Override
   public String toString() {
      return "AnimalDTO [kindDog=" + kindDog + ", kindEtc=" + kindEtc + ", ageN=" + ageN + ", weightN=" + weightN
            + ", neuterN=" + neuterN + ", sggGu=" + sggGu + ", sggSi=" + sggSi + "]";
   }
   

}