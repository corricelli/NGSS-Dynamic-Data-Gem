// DDG_Apps_Script.js (Simplified Automation Logic)

// CRITICAL: ID of your Control Sheet (Input Sheet)
const CONTROL_SHEET_ID = '1othRGkeNPnWQUpepGsNaM1F_OS-MWlDUdRND9-s7ul8';

// CRITICAL: The function that runs on a schedule (e.g., every 5 minutes)
function checkInputAndTriggerNotification() {
  
  // NOTE: This is the critical workaround for the Colab execution constraint.
  // We cannot programmatically run the Colab notebook from Apps Script alone.
  // Instead, we will notify the admin (the teacher) that a new request is pending.

  const ss = SpreadsheetApp.openById(CONTROL_SHEET_ID);
  const sheet = ss.getSheets();
  
  // Get the last row of data submitted by the web app/form
  const lastRow = sheet.getLastRow();
  
  // Check if there is data beyond the header row (assuming header is row 1)
  if (lastRow > 1) {
    // Get the PE_ID from the last request
    // Assumes PE_ID is in the second column (Column B, after Timestamp)
    const peIdRange = sheet.getRange(lastRow, 2);
    const peId = peIdRange.getValue();

    Logger.log('New DDG request found. PE ID: ' + peId);
    
    // Send an email notification to the teacher (you)
    const emailAddress = Session.getActiveUser().getEmail();
    const subject = 'DDG Request Pending: Manual Colab Run Required';
    const body = `A new data request has been submitted for PE ID: ${peId}.\n\n` +
                 `Please manually execute the "Generate Synthetic Data.ipynb" Colab notebook ` +
                 `to process the latest request (Row ${lastRow}).\n\n` +
                 `Control Sheet: ${ss.getUrl()}\n` +
                 `Colab Link: https://colab.research.google.com/drive/1eiOr8bUFBqGfd3Xcihh4D_CH-2VRjNo_?usp=sharing`;
    
    // **This is the key manual step:**
    // MailApp.sendEmail(emailAddress, subject, body); 
    Logger.log('Email notification prepared for manual Colab run.');

    // Optional: Mark the row as 'Pending' to prevent repeat notifications/processing
    // sheet.getRange(lastRow, 5).setValue('Pending'); 
  }
}
