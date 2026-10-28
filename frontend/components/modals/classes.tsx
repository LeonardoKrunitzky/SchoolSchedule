import Swal from 'sweetalert2';

export const showCreateClassModal = async () => {
  return Swal.fire({
    title: 'Nova Turma',
    width: '32em',
    html: `
      <input id="swal-name" class="swal2-input" placeholder="Nome da Turma (Ex: 1º Ano A)">
    `,
    focusConfirm: false,
    showCancelButton: true,
    confirmButtonText: 'Salvar',
    cancelButtonText: 'Cancelar',
    preConfirm: () => {
      const name = (document.getElementById('swal-name') as HTMLInputElement).value;
      
      if (!name) {
        Swal.showValidationMessage('O nome da turma é obrigatório');
        return false;
      }
      
      return { name };
    }
  });
};

export const showEditClassModal = async (turma: any) => {
  return Swal.fire({
    title: 'Editar Turma',
    width: '32em',
    html: `
      <input id="swal-name" class="swal2-input" value="${turma.name}" placeholder="Nome da Turma">
    `,
    showCancelButton: true,
    confirmButtonText: 'Atualizar',
    cancelButtonText: 'Cancelar',
    preConfirm: () => {
      const name = (document.getElementById('swal-name') as HTMLInputElement).value;
      
      if (!name) {
        Swal.showValidationMessage('O nome da turma é obrigatório');
        return false;
      }
      
      return { name };
    }
  });
};