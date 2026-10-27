import Image from 'next/image';
import Navbar from '@/components/navbar/Navbar';
import homeIllustration from '@/images/home.svg';
import './home.css';

export default function Home() {
  return (
    <main className="container">
      <Navbar />
      <div className="content">
        <h1>Sistema de Cronograma</h1>
        <p>Organize e gerencie o quadro de usuários e professores de forma simples e eficiente.</p>
        <Image
          src={homeIllustration}
          alt="Ilustração da página inicial"
          className="home-illustration"
          width={480}
          height={400}
          priority
        />
      </div>
    </main>
  );
}