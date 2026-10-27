"use client";

import React, { useState, useEffect } from "react";
import "./schedule.css";
import Navbar from "@/components/navbar/Navbar";

interface TeacherBlock {
  id: string;
  teacherName: string;
  color: string;
  rowId: string;
  startCol: number;
  durationCols: number;
  timeText: string;
}

const DIAS = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"];
const TURMAS = ["A1", "B1", "C1", "C2", "D1", "D/E", "Refeitório"];

const TIMES = [
  "06:00",
  "06:30",
  "07:00",
  "07:30",
  "08:00",
  "08:30",
  "09:00",
  "09:30",
  "10:00",
  "10:30",
  "11:00",
  "11:30",
  "12:00",
  "12:30",
  "13:00",
  "13:30",
  "14:00",
  "14:30",
  "15:00",
  "15:30",
  "16:00",
  "16:30",
  "17:00",
  "17:30",
  "18:00",
];

const TEACHERS = [
  "Gisele",
  "Nedi",
  "Fabi",
  "Pri",
  "Tielli",
  "Dacsi",
  "Leila",
  "Marceli",
  "Josiane",
  "Tais",
];

export default function GanttEscolar() {
  const [activeDay, setActiveDay] = useState(DIAS[0]);
  const [teacherColors, setTeacherColors] = useState<Record<string, string>>(
    {},
  );
  const [blocks, setBlocks] = useState<Record<string, TeacherBlock[]>>({});
  const [editingBlock, setEditingBlock] = useState<TeacherBlock | null>(null);

  useEffect(() => {
    const colors: Record<string, string> = {};
    TEACHERS.forEach((t) => {
      colors[t] = `hsl(${Math.floor(Math.random() * 360)}, 65%, 88%)`;
    });
    setTeacherColors(colors);
  }, []);

  // Inicia o arrasto da sidebar (Novo professor)
  const handleSidebarDragStart = (e: React.DragEvent, teacherName: string) => {
    e.dataTransfer.setData("source", "sidebar");
    e.dataTransfer.setData("teacherName", teacherName);
  };

  // Inicia o arrasto de um professor já na grade (Mover)
  const handleGridDragStart = (e: React.DragEvent, blockId: string) => {
    e.dataTransfer.setData("source", "grid");
    e.dataTransfer.setData("blockId", blockId);
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
  };

  const handleDrop = (e: React.DragEvent, rowId: string, colIndex: number) => {
    e.preventDefault();
    const source = e.dataTransfer.getData("source");

    if (source === "sidebar") {
      const teacherName = e.dataTransfer.getData("teacherName");
      if (!teacherName) return;

      const startTime = TIMES[colIndex] || "07:00";
      const endTime = TIMES[colIndex + 4] || "09:00"; // Duração padrão 2h

      const newBlock: TeacherBlock = {
        id: Math.random().toString(36).substring(2, 9),
        teacherName,
        color: teacherColors[teacherName] || "#e2e8f0",
        rowId,
        startCol: colIndex + 1,
        durationCols: 4,
        timeText: `${startTime} às ${endTime}`,
      };

      setBlocks((prev) => ({
        ...prev,
        [activeDay]: [...(prev[activeDay] || []), newBlock],
      }));
    } else if (source === "grid") {
      const blockId = e.dataTransfer.getData("blockId");
      setBlocks((prev) => {
        const dayBlocks = prev[activeDay] || [];
        const blockIndex = dayBlocks.findIndex((b) => b.id === blockId);
        if (blockIndex === -1) return prev;

        const block = dayBlocks[blockIndex];
        const newStartCol = colIndex + 1;

        // Recalcula o horário baseado na nova posição e na duração atual
        const startTime = TIMES[colIndex] || "07:00";
        const endIndex = Math.min(
          colIndex + block.durationCols,
          TIMES.length - 1,
        );
        const endTime = TIMES[endIndex] || "09:00";

        const updatedBlock = {
          ...block,
          rowId,
          startCol: newStartCol,
          timeText: `${startTime} às ${endTime}`,
        };

        const newDayBlocks = [...dayBlocks];
        newDayBlocks[blockIndex] = updatedBlock;
        return { ...prev, [activeDay]: newDayBlocks };
      });
    }
  };

  const saveEdit = () => {
    if (!editingBlock) return;

    const startSelect = document.getElementById(
      "edit-start",
    ) as HTMLSelectElement;
    const endSelect = document.getElementById("edit-end") as HTMLSelectElement;

    const startIndex = TIMES.indexOf(startSelect.value);
    const endIndex = TIMES.indexOf(endSelect.value);

    if (startIndex >= endIndex) {
      alert("O horário de fim deve ser depois do início.");
      return;
    }

    const newStartCol = startIndex + 1;
    const newDuration = endIndex - startIndex;

    setBlocks((prev) => {
      const dayBlocks = prev[activeDay] || [];
      const blockIndex = dayBlocks.findIndex((b) => b.id === editingBlock.id);
      if (blockIndex === -1) return prev;

      const newDayBlocks = [...dayBlocks];
      newDayBlocks[blockIndex] = {
        ...editingBlock,
        startCol: newStartCol,
        durationCols: newDuration,
        timeText: `${startSelect.value} às ${endSelect.value}`,
      };
      return { ...prev, [activeDay]: newDayBlocks };
    });
    setEditingBlock(null);
  };

  const deleteBlock = () => {
    if (!editingBlock) return;
    setBlocks((prev) => ({
      ...prev,
      [activeDay]: prev[activeDay].filter((b) => b.id !== editingBlock.id),
    }));
    setEditingBlock(null);
  };

  const currentDayBlocks = blocks[activeDay] || [];

  return (
    <div className="app-wrapper">
      <Navbar />
      <div className="layout-wrapper">
        <main className="gantt-main">
          <div className="tabs">
            {DIAS.map((dia) => (
              <button
                key={dia}
                className={`tab-btn ${activeDay === dia ? "active" : ""}`}
                onClick={() => setActiveDay(dia)}
              >
                {dia}
              </button>
            ))}
          </div>

          <div className="gantt-board">
            <div className="gantt-header">
              <div className="gantt-corner">Turmas</div>
              <div className="gantt-times">
                {TIMES.slice(0, -1).map((t) => (
                  <div key={t} className="time-cell">
                    {t}
                  </div>
                ))}
              </div>
            </div>

            <div className="gantt-body">
              {TURMAS.map((turma) => (
                <div key={turma} className="gantt-row">
                  <div className="row-label">{turma}</div>
                  <div className="row-grid">
                    {TIMES.slice(0, -1).map((_, idx) => (
                      <div
                        key={idx}
                        className="drop-cell"
                        style={{ gridColumn: idx + 1 }}
                        onDragOver={handleDragOver}
                        onDrop={(e) => handleDrop(e, turma, idx)}
                      />
                    ))}

                    {currentDayBlocks
                      .filter((b) => b.rowId === turma)
                      .map((block) => (
                        <div
                          key={block.id}
                          className="gantt-block"
                          draggable
                          onDragStart={(e) => handleGridDragStart(e, block.id)}
                          onClick={() => setEditingBlock(block)}
                          style={{
                            backgroundColor: block.color,
                            gridColumn: `${block.startCol} / span ${block.durationCols}`,
                          }}
                        >
                          <strong>{block.teacherName}</strong>
                          <span>{block.timeText}</span>
                        </div>
                      ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </main>

        <aside className="bottom-panel">
          <h3>Educadores</h3>
          <p>
            Arraste o nome do professor para a grade. Clique em um bloco na
            grade para editar o horário ou removê-lo.
          </p>
          <div className="teachers-list">
            {TEACHERS.map((t) => (
              <div
                key={t}
                draggable
                onDragStart={(e) => handleSidebarDragStart(e, t)}
                className="teacher-pill"
                style={{ backgroundColor: teacherColors[t] || "#eee" }}
              >
                {t}
              </div>
            ))}
          </div>
        </aside>

        {/* Modal de Edição (Redimensionar / Remover) */}
        {editingBlock && (
          <div className="modal-overlay" onClick={() => setEditingBlock(null)}>
            <div className="modal-content" onClick={(e) => e.stopPropagation()}>
              <h3>Editar Aula: {editingBlock.teacherName}</h3>
              <p className="modal-subtitle">
                Turma {editingBlock.rowId} - {activeDay}
              </p>

              <div className="modal-form">
                <div className="input-group">
                  <label>Início</label>
                  <select
                    id="edit-start"
                    defaultValue={editingBlock.timeText.split(" às ")[0]}
                  >
                    {TIMES.slice(0, -1).map((t) => (
                      <option key={t} value={t}>
                        {t}
                      </option>
                    ))}
                  </select>
                </div>
                <div className="input-group">
                  <label>Fim</label>
                  <select
                    id="edit-end"
                    defaultValue={editingBlock.timeText.split(" às ")[1]}
                  >
                    {TIMES.slice(1).map((t) => (
                      <option key={t} value={t}>
                        {t}
                      </option>
                    ))}
                  </select>
                </div>
              </div>

              <div className="modal-actions">
                <button className="btn-delete" onClick={deleteBlock}>
                  Remover da Grade
                </button>
                <div className="modal-actions-right">
                  <button
                    className="btn-cancel"
                    onClick={() => setEditingBlock(null)}
                  >
                    Cancelar
                  </button>
                  <button className="btn-save" onClick={saveEdit}>
                    Salvar Horário
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
