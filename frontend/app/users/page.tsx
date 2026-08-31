'use client';
import { useEffect, useState } from 'react';
import Swal from 'sweetalert2';
import styles from './users.module.css';
import { showCreateUserModal, showEditUserModal } from '@/components/modals/users';
import Navbar from '@/components/navbar/Navbar';
import { getUsers, getRoles, createUser, updateUser, toggleUserStatus } from '@/services/users';

export default function Users() {
  const [users, setUsers] = useState<any[]>([]);
  const [roles, setRoles] = useState<any[]>([]);

  const loadData = async () => {
    try {
      const [usersData, rolesData] = await Promise.all([getUsers(), getRoles()]);
      setUsers(usersData);
      setRoles(rolesData);
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleCreate = async () => {
    if (roles.length === 0) {
      Swal.fire('Aviso', 'Os cargos ainda estão sendo carregados ou houve um erro na API.', 'warning');
      return;
    }

    const result = await showCreateUserModal(roles);
    if (result.isConfirmed) {
      try {
        await createUser(result.value);
        loadData();
        Swal.fire('Criado!', 'Professor cadastrado com sucesso.', 'success');
      } catch (error) {
        Swal.fire('Erro!', 'Falha ao criar o professor.', 'error');
      }
    }
  };

  const handleEdit = async (user: any) => {
    const result = await showEditUserModal(user);
    if (result.isConfirmed) {
      try {
        await updateUser(user.id, result.value);
        loadData();
        Swal.fire('Atualizado!', 'Dados do professor atualizados.', 'success');
      } catch (error) {
        Swal.fire('Erro!', 'Falha ao atualizar o professor.', 'error');
      }
    }
  };

  const handleToggleStatus = async (id: string) => {
    try {
      await toggleUserStatus(id);
      loadData();
    } catch (error) {
      Swal.fire('Erro', 'Não foi possível alterar o status', 'error');
    }
  };

  return (
    <main className={styles.page}>
      <Navbar />
      <div className={styles.container}>
        <div className={styles.header}>
          <h2>Gestão de Professores</h2>
          <button className={styles.createBtn} onClick={handleCreate}>+ Novo Professor</button>
        </div>
        
        <div className={styles.tableWrapper}>
          <table className={styles.table}>
            <thead>
              <tr>
                <th>Nome</th>
                <th>Matrícula</th>
                <th>Período</th>
                <th>Status</th>
                <th>Ações</th>
              </tr>
            </thead>
            <tbody>
              {users.map(user => (
                <tr key={user.id}>
                  <td>{user.name}</td>
                  <td>{user.registration}</td>
                  <td>{user.period || '-'}</td>
                  <td>
                    <span className={user.status ? styles.active : styles.inactive}>
                      {user.status ? 'Ativo' : 'Inativo'}
                    </span>
                  </td>
                  <td className={styles.actions}>
                    <button onClick={() => handleEdit(user)} className={styles.editBtn}>Editar</button>
                    <button onClick={() => handleToggleStatus(user.id)} className={styles.toggleBtn}>Ativar/Desativar</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </main>
  );
}