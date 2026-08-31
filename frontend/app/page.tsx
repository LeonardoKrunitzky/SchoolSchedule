import Navbar from '@/components/navbar/Navbar';
import styles from './home.module.css';

export default function Home() {
  return (
    <main className={styles.container}>
      <Navbar />
      <div className={styles.content}>
        <h1>Sistema de Cronograma</h1>
        <p>Organize e gerencie o quadro de usuários e professores de forma simples e eficiente.</p>
      </div>
    </main>
  );
}