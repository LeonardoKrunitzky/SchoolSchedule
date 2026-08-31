'use client';
import { useForm } from 'react-hook-form';
import { useRouter } from 'next/navigation';
import styles from './login.module.css';
import Swal from 'sweetalert2';
import { useEffect } from 'react';
import Navbar from '@/components/navbar/Navbar';
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
      
      const token = response?.token || 'autenticado';
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
    <main className={styles.page}>
      <Navbar />
      <div className={styles.formContainer}>
        <h2>Acessar Sistema</h2>
        <form onSubmit={handleSubmit(onSubmit)} className={styles.form}>
          <div className={styles.inputGroup}>
            <label>Matrícula</label>
            <input type="text" {...register('registration', { required: true })} />
            {errors.registration && <span>Campo obrigatório</span>}
          </div>
          <div className={styles.inputGroup}>
            <label>Senha</label>
            <input type="password" {...register('password', { required: true })} />
            {errors.password && <span>Campo obrigatório</span>}
          </div>
          <button type="submit" className={styles.submitBtn}>Entrar</button>
        </form>
      </div>
    </main>
  );
}