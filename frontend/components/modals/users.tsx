import Swal from 'sweetalert2';

export const showCreateUserModal = async (roles: any[]) => {
  return Swal.fire({
    title: 'Novo Usuário',
    width: '32em',
    html: `
      <style>
        .custom-radio-group {
          display: flex;
          flex-wrap: wrap;
          justify-content: center;
          gap: 0.5rem;
          margin: 0.5rem auto 1.5rem auto;
          width: 90%;
        }
        .custom-radio-label {
          display: flex;
          flex: 1;
          align-items: center;
          justify-content: center;
          gap: 0.5rem;
          padding: 0.6rem;
          border: 1px solid #d9d9d9;
          border-radius: 6px;
          cursor: pointer;
          font-size: 0.9rem;
          color: #545454;
          transition: all 0.2s ease;
          min-width: 80px;
        }
        .custom-radio-label:hover {
          border-color: #111;
        }
        .custom-radio-label:has(input:checked) {
          border-color: #111;
          background-color: #fafafa;
          font-weight: 600;
          color: #111;
        }
        .custom-radio-label input {
          display: none;
        }
        .section-title {
          text-align: left;
          width: 90%;
          margin: 1rem auto 0.2rem;
          font-weight: 500;
          color: #444;
          font-size: 0.85rem;
        }
      </style>

      <input id="swal-name" class="swal2-input" placeholder="Nome Completo">
      <input type="number" id="swal-reg" class="swal2-input" placeholder="Matrícula (Apenas números)">
      
      <div class="section-title">Cargo:</div>
      <div class="custom-radio-group">
        ${roles.map(role => `
          <label class="custom-radio-label">
            <input type="radio" name="swal-role" value="${role.id}"> 
            ${role.name}
          </label>
        `).join('')}
      </div>

      <div class="section-title">Período:</div>
      <div class="custom-radio-group">
        <label class="custom-radio-label">
          <input type="radio" name="swal-period" value="Manhã" checked> Manhã
        </label>
        <label class="custom-radio-label">
          <input type="radio" name="swal-period" value="Tarde"> Tarde
        </label>
        <label class="custom-radio-label">
          <input type="radio" name="swal-period" value="Noite"> Noite
        </label>
      </div>

      <input type="number" id="swal-workload" class="swal2-input" placeholder="Carga Horária (h)">
      <input type="password" id="swal-pass" class="swal2-input" placeholder="Senha">
    `,
    focusConfirm: false,
    showCancelButton: true,
    confirmButtonText: 'Salvar',
    cancelButtonText: 'Cancelar',
    preConfirm: () => {
      const name = (document.getElementById('swal-name') as HTMLInputElement).value;
      const registration = (document.getElementById('swal-reg') as HTMLInputElement).value;
      const roleElement = document.querySelector('input[name="swal-role"]:checked') as HTMLInputElement;
      const role_id = roleElement ? roleElement.value : null;
      const periodElement = document.querySelector('input[name="swal-period"]:checked') as HTMLInputElement;
      const period = periodElement ? periodElement.value : null;
      const workload = parseInt((document.getElementById('swal-workload') as HTMLInputElement).value) || 0;
      const password = (document.getElementById('swal-pass') as HTMLInputElement).value;
      
      if (!name || !registration || !role_id || !password) {
        Swal.showValidationMessage('Preencha os campos obrigatórios (Nome, Matrícula, Cargo e Senha)');
        return false;
      }
      
      return { name, registration, role_id, period, workload, password };
    }
  });
};

export const showEditUserModal = async (user: any) => {
  return Swal.fire({
    title: 'Editar Usuário',
    html: `
      <input id="swal-name" class="swal2-input" value="${user.name}" placeholder="Nome">
      <input id="swal-period" class="swal2-input" value="${user.period || ''}" placeholder="Período/Turno">
      <input type="number" id="swal-workload" class="swal2-input" value="${user.workload || ''}" placeholder="Carga Horária (h)">
    `,
    showCancelButton: true,
    confirmButtonText: 'Atualizar',
    cancelButtonText: 'Cancelar',
    preConfirm: () => {
      const name = (document.getElementById('swal-name') as HTMLInputElement).value;
      const period = (document.getElementById('swal-period') as HTMLInputElement).value;
      const workload = parseInt((document.getElementById('swal-workload') as HTMLInputElement).value) || 0;
      
      if (!name) {
        Swal.showValidationMessage('O nome é obrigatório');
        return false;
      }
      return { name, period, workload };
    }
  });
};