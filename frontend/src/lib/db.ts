import Dexie, { Table } from 'dexie';

export interface SyncQueueItem {
  localId?: number;
  entityType: string;
  entityId: string;
  action: 'create' | 'update' | 'delete';
  payload: Record<string, unknown>;
  timestamp: number;
  status: 'pending' | 'synced' | 'failed';
}

class SIHDatabase extends Dexie {
  syncQueue!: Table<SyncQueueItem>;

  constructor() {
    super('sih_db');
    this.version(1).stores({
      syncQueue: '++localId, entityType, entityId, status, timestamp',
    });
  }
}

export const db = new SIHDatabase();
