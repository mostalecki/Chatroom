export interface RoomListConfig {
  type: string;

  filters: {
    name?: string;
    limit?: number;
    offset?: number;
  };
}
