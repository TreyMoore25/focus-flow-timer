/**
 * Focus Flow — append focus sessions to this spreadsheet.
 * SETUP
 * 1. Create a new Google Sheet (or open an existing one).
 * 2. Extensions → Apps Script → paste this entire file → Save.
 * 3. Click Deploy → New deployment → Type: Web app
 *    - Execute as: Me
 *    - Who has access: Anyone (needed for POST from your timer page)
 * 4. Copy the Web app URL (ends with /exec) into the timer’s “Google Sheet sync” field.
 *
 * The first POST will create a header row if the sheet is empty.
 */
function doPost(e) {
  const lock = LockService.getDocumentLock();
  lock.waitLock(30000);
  try {
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheets()[0];
    if (sheet.getLastRow() === 0) {
      sheet.appendRow([
        'Start (ISO)',
        'End (ISO)',
        'Duration (min)',
        'Note',
        'Day',
        'Session ID',
        'Logged at (ISO)'
      ]);
    }
    var raw = e.postData && e.postData.contents ? e.postData.contents : '{}';
    var data = JSON.parse(raw);
    sheet.appendRow([
      data.startIso || '',
      data.endIso || '',
      data.durationMin != null ? data.durationMin : '',
      data.note || '',
      data.dayKey || '',
      data.id || '',
      data.createdIso || new Date().toISOString()
    ]);
    return ContentService
      .createTextOutput(JSON.stringify({ ok: true }))
      .setMimeType(ContentService.MimeType.JSON);
  } catch (err) {
    return ContentService
      .createTextOutput(JSON.stringify({ ok: false, error: String(err) }))
      .setMimeType(ContentService.MimeType.JSON);
  } finally {
    lock.releaseLock();
  }
}

function doGet() {
  return ContentService
    .createTextOutput(JSON.stringify({ ok: true, message: 'Focus Flow sheet endpoint is running. Use POST to append rows.' }))
    .setMimeType(ContentService.MimeType.JSON);
}
