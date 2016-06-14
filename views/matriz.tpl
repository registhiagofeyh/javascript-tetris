<table>
	% line = 1
	% for linha in tabela:
		<tr>
			<th>{{line}}:</th>
		%for coluna in linha:
			<td>{{coluna}}</td>
		%end
		% line += 1
		</tr>
	%end
</table>