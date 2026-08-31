import Link from 'next/link';
import styles from './Navbar.module.css';

export default function Navbar() {
  return (
    <nav className={styles.navbar}>
      <div className={styles.brand}>Cronograma Escolar</div>
      <ul className={styles.links}>
        <li><Link href="/">Início</Link></li>
        <li><Link href="/users">Funcionários</Link></li>
      </ul>
    </nav>
  );
}