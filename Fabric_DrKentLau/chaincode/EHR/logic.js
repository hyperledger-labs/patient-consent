'use strict';
const { Contract} = require('fabric-contract-api');

class ehr extends Contract {



   async queryRecord(ctx,patientId) {
   
    let marksAsBytes = await ctx.stub.getState(patientId); 
    if (!marksAsBytes || marksAsBytes.toString().length <= 0) {
      throw new Error('Patient with this Id does not exist: ');
       }
      let marks=JSON.parse(marksAsBytes.toString());

      return JSON.stringify(marks);
     }

   async addRecord(ctx,patientId,data1,data2,data3,data4,data5,data6,data7,data8,data9) {
   
    let marks={
       age:data1,
       sex:data2,
       bmi:data3,
       hbA1c:data4,
       concomitant_medication:data5,
       history_of_cancer:data6,
       race:data7,
       diagnosis_over_1year:data8,
       childbirth_potential:data9
       };

    await ctx.stub.putState(patientId,Buffer.from(JSON.stringify(marks))); 
    
    console.log('Patient Record added To the ledger Succesfully..');
    
  }

   async deleteRecord(ctx,patientId) {
   

    await ctx.stub.deleteState(patientId); 
    
    console.log('Student Marks deleted from the ledger Succesfully..');
    
    }
}

module.exports=ehr;
