'use client';
import { useEffect, useState } from 'react';
import Swal from 'sweetalert2';
import './classes.css';
import { showCreateClassModal, showEditClassModal } from '@/components/modals/classes';
import Navbar from '@/components/navbar/Navbar';
import { getClasses, createClass, updateClass, deleteClass } from '@/services/classes';

/**
 * Renders the Classes management page.
 * Displays a table of classes and handles creation, edition, and deletion.
 */
export default function Classes() {
  const [classes, setClasses] = useState<any[]>([]);

  /**
   * Fetches the classes from the API and updates the state.
   */
  const loadData = async () => {
    try {
      const data = await getClasses();
      setClasses(data);
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  /**
   * Opens the creation modal and triggers the API call to create a new class.
   */
  const handleCreate = async () => {
    const result = await showCreateClassModal();
    if (result.isConfirmed) {
      try {
        await createClass(result.value);
        loadData();
        Swal.fire('Criado!', 'Turma cadastrada com sucesso.', 'success');
      } catch (error) {
        Swal.fire('Erro!', 'Falha ao criar a turma.', 'error');
      }
    }
  };

  /**
   * Opens the edit modal and triggers the API call to update an existing class.
   * @param {any} turma - The class object to edit.
   */
  const handleEdit = async (turma: any) => {
    const result = await showEditClassModal(turma);
    if (result.isConfirmed) {
      try {
        await updateClass(turma.id, result.value);
        loadData();
        Swal.fire('Atualizado!', 'Dados da turma atualizados.', 'success');
      } catch (error) {
        Swal.fire('Erro!', 'Falha ao atualizar a turma.', 'error');
      }
    }
  };

  /**
   * Prompts for confirmation and triggers the API call to delete a class.
   * @param {string} id - The class ID to delete.
   */
  const handleDelete = async (id: string) => {
    const result = await Swal.fire({
      title: 'Tem certeza?',
      text: 'Esta ação removerá a turma permanentemente!',
      icon: 'warning',
      showCancelButton: true,
      confirmButtonText: 'Sim, excluir',
      cancelButtonText: 'Cancelar'
    });

    if (result.isConfirmed) {
      try {
        await deleteClass(id);
        loadData();
        Swal.fire('Excluído!', 'Turma removida com sucesso.', 'success');
      } catch (error) {
        Swal.fire('Erro', 'Não foi possível excluir a turma.', 'error');
      }
    }
  };

  return (
    <main className="page">
      <Navbar/>
      <div className="container">
        <div className="header">
          <h2>Gestão de Turmas</h2>
          <button className="createBtn" onClick={handleCreate}>+ Nova Turma</button>
        </div>

        <div className="tableWrapper">
          <table className="table">
            <thead>
              <tr>
                <th>Nome</th>
                <th className="actions-header">Ações</th>
              </tr>
            </thead>
            <tbody>
              {classes.map(turma => (
                <tr key={turma.id}>
                  <td>{turma.name}</td>
                  <td className="actions">
                    <button onClick={() => handleEdit(turma)} className="editBtn">Editar</button>
                    <button onClick={() => handleDelete(turma.id)} className="deleteBtn">Excluir</button>
                  </td>
                </tr>
              ))}
              {classes.length === 0 && (
                <tr>
                  <td colSpan={2} className="empty-state">Nenhuma turma encontrada.</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </main>
  );
}