package simpledb.tx.concurrency;

import simpledb.file.Block;
import java.util.*;

/**
 * The lock table, which provides methods to lock and unlock blocks.
 * If a transaction requests a lock that causes a conflict with an
 * existing lock, then that transaction is placed on a wait list.
 * There is only one wait list for all blocks.
 * When the last lock on a block is unlocked, then all transactions
 * are removed from the wait list and rescheduled.
 * If one of those transactions discovers that the lock it is waiting for
 * is still locked, it will place itself back on the wait list.
 * @author Edward Sciore
 */
class LockTable {
   private static final long MAX_TIME = 50; // 10 seconds
   
   private Map<Block,List<Integer>> locks = new HashMap<>();
   
   /**
    * Grants an SLock on the specified block.
    * If an XLock exists when the method is called,
    * then the calling thread will be placed on a wait list
    * until the lock is released.
    * If the thread remains on the wait list for a certain 
    * amount of time (currently 10 seconds),
    * then an exception is thrown.
    * @param blk a reference to the disk block
    */
   public synchronized void sLock(Block blk, int txnum) {
      try {
         long timestamp = System.currentTimeMillis();
         while (hasXlock(blk)) {
            List<Integer> list = getLockList(blk);
            for (int i : list) {
               if (Math.abs(i) < txnum) 
                  throw new InterruptedException();
            }
            wait(MAX_TIME);
         }
         locks.putIfAbsent(blk, new ArrayList<>());
         locks.get(blk).add(txnum);
      }
      catch(InterruptedException e) {
         throw new LockAbortException();
      }
   }
   
   /**
    * Grants an XLock on the specified block.
    * If a lock of any type exists when the method is called,
    * then the calling thread will be placed on a wait list
    * until the locks are released.
    * If the thread remains on the wait list for a certain 
    * amount of time (currently 10 seconds),
    * then an exception is thrown.
    * @param blk a reference to the disk block
    */
   synchronized void xLock(Block blk, int txnum) {
      try {
         long timestamp = System.currentTimeMillis();
         while (hasOtherSLocks(blk) && !waitingTooLong(timestamp)) {
            List<Integer> list = getLockList(blk);
            for (int i : list) {
               if (Math.abs(i) < txnum) 
                  throw new InterruptedException();
            }
            // wait(MAX_TIME);
         }
         locks.putIfAbsent(blk, new ArrayList<>());
         locks.get(blk).add(-txnum);
      }
      catch(InterruptedException e) {
         throw new LockAbortException();
      }
   }
   
   /**
    * Releases a lock on the specified block.
    * If this lock is the last lock on that block,
    * then the waiting transactions are notified.
    * @param blk a reference to the disk block
    */
   synchronized void unlock(Block blk, int txnum) {
      List<Integer> list = getLockList(blk);
      list.remove(new Integer(txnum));
      list.remove(new Integer(-txnum));
      if (list.size() == 0)
         notifyAll();
   }
   
   private boolean hasXlock(Block blk) {
      List<Integer> list = getLockList(blk);
      if (list == null) return false;
      for (int i : list) {
         if (i < 0) return true;
      }
      return false;
   }
   
   private boolean hasOtherSLocks(Block blk) {
      List<Integer> list = getLockList(blk);
      if (list == null) return false;
      for (int i : list) {
         if (i > 1) return true;
      }
      return false;
   }
   
   private boolean waitingTooLong(long starttime) {
      return System.currentTimeMillis() - starttime > MAX_TIME;
   }
   
   // private int getLockVal(Block blk) {
   //    Integer ival = locks.get(blk);
   //    return (ival == null) ? 0 : ival.intValue();
   // }

   private List<Integer> getLockList(Block blk) {
      List<Integer> list = locks.get(blk);
      return (list == null || list.size() == 0) ? null : list;
   }

   public void release() {
      locks.clear();
   }
}
