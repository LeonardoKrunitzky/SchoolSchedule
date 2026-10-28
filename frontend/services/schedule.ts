import { api } from "./base";

export interface ClassRoom {
  id: string;
  name: string;
}

export interface ScheduleRecord {
  id: string;
  user_id: string;
  class_id: string;
  weekday: number;
  start_time: string;
  end_time: string;
  observation?: string;
  is_fixed?: boolean;
}

export interface CreateScheduleDTO {
  user_id: string;
  class_id: string;
  weekday: number;
  start_time: string;
  end_time: string;
  observation?: string;
  is_fixed?: boolean;
}

/**
 * Retrieves all fixed availability schedule records.
 * 
 * @returns A promise that resolves to an array of ScheduleRecord objects.
 */
export async function getSchedules(): Promise<ScheduleRecord[]> {
  const response = await api.get<ScheduleRecord[]>('/fixed-availability');
  return response.data;
}

/**
 * Creates a new schedule record for a teacher.
 * 
 * @param data - The schedule record details excluding the ID.
 * @returns A promise that resolves to the created ScheduleRecord.
 */
export async function createSchedule(data: CreateScheduleDTO): Promise<ScheduleRecord> {
  const response = await api.post<ScheduleRecord>('/fixed-availability', data);
  return response.data;
}

/**
 * Updates an existing schedule record.
 * 
 * @param id - The unique identifier of the schedule record.
 * @param data - The updated schedule record details.
 * @returns A promise that resolves to the updated ScheduleRecord.
 */
export async function updateSchedule(id: string, data: Partial<CreateScheduleDTO>): Promise<ScheduleRecord> {
  const response = await api.put<ScheduleRecord>(`/fixed-availability/${id}`, data);
  return response.data;
}

/**
 * Deletes a schedule record by its ID.
 * 
 * @param id - The unique identifier of the schedule record to delete.
 */
export async function deleteSchedule(id: string): Promise<void> {
  await api.delete(`/fixed-availability/${id}`);
}