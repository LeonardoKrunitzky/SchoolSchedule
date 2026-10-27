'use client';
import { useForm } from 'react-hook-form';
import { useRouter } from 'next/navigation';
import './login.css';
import Swal from 'sweetalert2';
import { useEffect } from 'react';
import { login } from '@/services/users';

export default function Login() {
  const { register, handleSubmit, formState: { errors } } = useForm();
  const router = useRouter();

  useEffect(() => {
    document.cookie = 'auth-token=; path=/; max-age=0';
  }, []);

  const onSubmit = async (data: any) => {
    try {
      const response = await login(data);

      const token = response?.access_token;

      if (!token) {
        throw new Error('Token não encontrado na resposta');
      }

      document.cookie = `auth-token=${token}; path=/; max-age=86400`;

      Swal.fire({
        title: 'Sucesso',
        text: 'Login realizado com sucesso!',
        icon: 'success',
        timer: 1500,
        showConfirmButton: false
      });

      router.push('/');
    } catch (error) {
      Swal.fire('Erro', 'Credenciais inválidas', 'error');
    }
  };

  return (
    <main className="page">
      <div className="formContainer">
        <h2>Acessar Sistema</h2>
        <form onSubmit={handleSubmit(onSubmit)} className="form">
          <div className="inputGroup">
            <label>Matrícula</label>
            <input type="text" {...register('registration', { required: true })} />
            {errors.registration && <span>Campo obrigatório</span>}
          </div>
          <div className="inputGroup">
            <label>Senha</label>
            <input type="password" {...register('password', { required: true })} />
            {errors.password && <span>Campo obrigatório</span>}
          </div>
          <button type="submit" className="submitBtn">Entrar</button>
        </form>
      </div>
    </main>
  );
}