'use strict';
const { Contract} = require('fabric-contract-api');

class ehr extends Contract {



   async queryRecord(ctx,patientId) {
   
    let dataAsBytes = await ctx.stub.getState(patientId); 
    if (!dataAsBytes || dataAsBytes.toString().length <= 0) {
      throw new Error('PATIENT WITH THIS ID DOES NOT EXIST: ');
       }
      let data=JSON.parse(dataAsBytes.toString());
      
      return JSON.stringify(data);
     }

   async addRecord(ctx,patientId,data1,data2,data3,data4,data5,data6,data7,data8,data9) {
   
    let data={
      '000-IDENTITY':patientId,
      '001-AGE':data1,
      '002-SEX':data2,
      '003-BMI':data3,
      '004-HBA1C':data4,
      '005-CONCOMITANT_MEDICATION':data5,
      '006-HISTORY_OF_CANCER':data6,
      '007-RACE':data7,
      '008-DIAGNOSIS_OVER_1YEAR':data8,
      '009-CHILDBIRTH_POTENTIAL':data9
       };

    await ctx.stub.putState(patientId,Buffer.from(JSON.stringify(data))); 
    
    console.log('PATIENT RECORD ADDED TO THE LEDGER SUCCESSFULLY!');
    
  }

   async deleteRecord(ctx,patientId) {
   

    await ctx.stub.deleteState(patientId); 
    
    console.log('PATIENT RECORD DELETED FROM THE LEDGER SUCCESSFULLY!');
    
    }
}

module.exports=ehr;
