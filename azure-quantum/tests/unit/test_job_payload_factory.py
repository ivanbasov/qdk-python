##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##

import pytest
import unittest
from typing import TYPE_CHECKING, Union, Tuple
from import_qsharp import skip_if_no_qsharp

if TYPE_CHECKING:
    import cirq
    import qiskit
    import azure.quantum.optimization as optimization
    from qsharp import QSharpCallable


class JobPayloadFactory():
    @staticmethod
    def get_cirq_circuit_bell_state() -> "cirq.Circuit":
        import cirq
        q0 = cirq.LineQubit(0)
        q1 = cirq.LineQubit(1)
        circuit = cirq.Circuit(
            cirq.H(q0),
            cirq.CNOT(q0, q1),
            cirq.measure(q0, key='q0'),
            cirq.measure(q1, key='q1')
        )
        return circuit

    @staticmethod
    def get_qsharp_inline_code_bell_state() -> Tuple[str, str]:
        return ("""
        open Microsoft.Quantum.Intrinsic;

        operation BellState_Inline() : (Result,Result) {
            use q0 = Qubit();
            use q1 = Qubit();
            H(q0);
            CNOT(q0, q1);
            return (M(q0), M(q1));
        }
        """, "ENTRYPOINT__BellState_Inline")

    qsharp_inline_callable_bell_state = None

    @staticmethod
    def get_qsharp_inline_callable_bell_state() -> Tuple["QSharpCallable", str]:
        if not JobPayloadFactory.qsharp_inline_callable_bell_state:
            (qsharp_code, entrypoint) = JobPayloadFactory.get_qsharp_inline_code_bell_state()
            import qsharp
            JobPayloadFactory.qsharp_inline_callable_bell_state = (qsharp.compile(qsharp_code), entrypoint)
        return JobPayloadFactory.qsharp_inline_callable_bell_state

    @staticmethod
    def get_qsharp_inline_qir_bitcode_bell_state(target: Union[None, str] = None) -> Tuple[bytes, str]:
        (qsharpCallable, entrypoint) = JobPayloadFactory.get_qsharp_inline_callable_bell_state()
        qir_bitcode = qsharpCallable._repr_qir_(target=target)
        return (qir_bitcode, entrypoint)

    qsharp_file_callable_bell_state = None

    @staticmethod
    def get_qsharp_file_callable_bell_state() -> Tuple["QSharpCallable", str]:
        if not JobPayloadFactory.qsharp_file_callable_bell_state:
            from QSharpBellState import BellState_File
            JobPayloadFactory.qsharp_file_callable_bell_state = (BellState_File, "BellState_File")
        return JobPayloadFactory.qsharp_file_callable_bell_state

    qsharp_file_qir_bitcode_bell_state = None

    @staticmethod
    def get_qsharp_file_qir_bitcode_bell_state(target: Union[None, str] = None) -> Tuple[bytes, str]:
        if not JobPayloadFactory.qsharp_file_qir_bitcode_bell_state:
            (qsharpCallable, entrypoint) = JobPayloadFactory.get_qsharp_file_callable_bell_state()
            qir_bitcode = qsharpCallable._repr_qir_(target=target)
            JobPayloadFactory.qsharp_file_qir_bitcode_bell_state = (qir_bitcode, entrypoint)
        return JobPayloadFactory.qsharp_file_qir_bitcode_bell_state

    @staticmethod
    def get_qiskit_circuit_bell_state() -> "qiskit.QuantumCircuit":
        from qiskit import QuantumCircuit
        circuit = QuantumCircuit(2, 2)
        circuit.name = "BellState"
        circuit.h(0)
        circuit.cnot(0, 1)
        circuit.measure([0, 1], [0, 1])
        return circuit


class TestJobPayloadFactory(unittest.TestCase):
    @pytest.mark.cirq
    def test_get_cirq_circuit_bell_state(self):
        import cirq
        self.assertIsInstance(JobPayloadFactory.get_cirq_circuit_bell_state(), cirq.Circuit)

    @pytest.mark.qiskit
    def test_get_qiskit_circuit_bell_state(self):
        import qiskit
        self.assertIsInstance(JobPayloadFactory.get_qiskit_circuit_bell_state(), qiskit.QuantumCircuit)

    @pytest.mark.qsharp
    @skip_if_no_qsharp
    def test_get_qsharp_inline_callable_bell_state(self):
        from qsharp import QSharpCallable
        result = JobPayloadFactory.get_qsharp_inline_callable_bell_state()
        self.assertIsInstance(result, Tuple)
        self.assertIsInstance(result[0], QSharpCallable)
        self.assertIsInstance(result[1], str)

    @pytest.mark.qsharp
    @pytest.mark.qir
    @skip_if_no_qsharp
    def test_get_qsharp_inline_qir_bell_state(self):
        result = JobPayloadFactory.get_qsharp_inline_qir_bitcode_bell_state()
        self.assertIsInstance(result, Tuple)
        self.assertIsInstance(result[0], bytes)
        self.assertIsInstance(result[1], str)

    @pytest.mark.qsharp
    @skip_if_no_qsharp
    def test_get_qsharp_file_callable_bell_state(self):
        from qsharp import QSharpCallable
        result = JobPayloadFactory.get_qsharp_file_callable_bell_state()
        self.assertIsInstance(result, Tuple)
        self.assertIsInstance(result[0], QSharpCallable)
        self.assertIsInstance(result[1], str)

    @pytest.mark.qsharp
    @pytest.mark.qir
    @skip_if_no_qsharp
    def test_get_qsharp_file_qir_bell_state(self):
        result = JobPayloadFactory.get_qsharp_file_qir_bitcode_bell_state()
        self.assertIsInstance(result, Tuple)
        self.assertIsInstance(result[0], bytes)
        self.assertIsInstance(result[1], str)
