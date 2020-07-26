package simpledb.tx.recovery;

import simpledb.log.BasicLogRecord;

import java.util.HashSet;

/**
 * The NQ CHECKPOINT log record.
 * @author Geng Yang
 */
class NQCheckpoint implements LogRecord {

   private HashSet<Integer> activeTransactions;
   
   /**
    * Creates a non quiescent checkpoint record.
    */
   public NQCheckpoint() {
      activeTransactions = new HashSet<>();
   }
   
   /**
    * Creates a log record by reading no other values 
    * from the basic log record.
    * @param rec the basic log record
    */
   public NQCheckpoint(BasicLogRecord rec) {
      activeTransactions = new HashSet<>();
   }

   /**
    * Creates a non quiescent checkpoint record.
    */
   public NQCheckpoint(HashSet<Integer> activeTransactions) {
      this.activeTransactions = activeTransactions;
   }
   
   /** 
    * Writes a nq checkpoint record to the log.
    * This log record contains the CHECKPOINT operator,
    * and nothing else.
    * @return the LSN of the last log value
    */
   public int writeToLog() {
      Object[] rec = new Object[activeTransactions.size() + 1];
      rec[0] = NQCHECKPOINT;
      int i = 1;
      for (int tx : activeTransactions)
         rec[i++] = tx;
      return logMgr.append(rec);
   }
   
   public int op() {
      return NQCHECKPOINT;
   }
   
   /**
    * NQ Checkpoint records have no associated transaction,
    * and so the method returns a "dummy", negative txid.
    */
   public int txNumber() {
      return -1; // dummy value
   }
   
   /**
    * Does nothing, because a nq checkpoint record
    * contains no undo information.
    */
   public void undo(int txnum) {}
   
   public String toString() {
      String val = "<NQCHECKPOINT ";
      for (int i : activeTransactions) 
         val += (i + " ");
      val += ">";
      return val;
   }
}
