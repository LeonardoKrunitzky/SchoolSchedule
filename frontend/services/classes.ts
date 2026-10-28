import { api } from "./base";

/**
 * Retrieves a list of all classes from the API.
 * 
 * @returns A promise that resolves to the array of classes.
 */
export async function getClasses() {
  const response = await api.get('/classes/');
  return response.data;
}

/**
 * Creates a new class with the provided name.
 * 
 * @param data The payload containing the class name.
 * @returns A promise resolving to the created class data.
 */
export async function createClass(data: { name: string }) {
  const response = await api.post('/classes/', data);
  return response.data;
}

/**
 * Updates the name of an existing class.
 * 
 * @param classId The unique identifier of the class.
 * @param data The payload containing the new class name.
 * @returns A promise resolving to the updated class data.
 */
export async function updateClass(classId: string, data: { name: string }) {
  const response = await api.put(`/classes/${classId}`, data);
  return response.data;
}

/**
 * Deletes a class from the system.
 * 
 * @param classId The unique identifier of the class to be deleted.
 * @returns A promise resolving to the API response.
 */
export async function deleteClass(classId: string) {
  const response = await api.delete(`/classes/${classId}`);
  return response.data;
}