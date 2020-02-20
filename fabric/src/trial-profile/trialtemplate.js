'use strict';
const { Contract} = require('fabric-contract-api');

class PreConsentTrailProfile extends Contract {



   async queryRecord(ctx,) {

    let dataAsBytes = await ctx.stub.getState(preConsentTrialId);
    if (!dataAsBytes || dataAsBytes.toString().length <= 0) {
      throw new Error('TRIAL WITH THIS ID DOES NOT EXIST: ');
       }
      let data=JSON.parse(dataAsBytes.toString());

      return JSON.stringify(data);
     }

   async addRecord(ctx,preConsentTrialId,data1,data2,data3) {

    let data={
      '000-TRIALIDENTITY':preConsentTrialId,
      '001-PHASE':data1,
      '002-PRININVESTIGATOR':data2,
      '003-TRIALLOCATION':data3
       };

    await ctx.stub.putState(preConsentTrialId,Buffer.from(JSON.stringify(data)));

    console.log('TRIAL RECORD ADDED TO THE LEDGER SUCCESSFULLY!');

  }

   async deleteRecord(ctx,preConsentTrialId) {


    await ctx.stub.deleteState(preConsentTrialId);

    console.log('TRIAL RECORD DELETED FROM THE LEDGER SUCCESSFULLY!');

    }
}

export default PreConsentTrialProfile;
