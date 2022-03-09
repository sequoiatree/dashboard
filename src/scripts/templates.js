function compile(template) {

    return Handlebars.compile(
        (
            template
            .split('\n')
            .map(
                function(line) {
                    line = line.replace(/^\s+/, '');
                    line = line.replace(/\s+$/, '');
                    return line;
                }
            )
            .join('')
        ),
        {
            strict: true,
        },
    );

}

export const UPLOAD_CONTENT_TEMPLATE = compile(`
<div id="{{id}}-content" class="upload-content m-3">
  {{{content}}}
</div>
`);

export const UPLOAD_BUTTON_TEMPLATE = compile(`
<div class="d-flex flex-column justify-content-center h-100">
  <div class="mx-1 px-3 py-2 text-center text-uppercase text-unselectable font-family-serif">
    Drag and drop files or click to select.
  </div>
</div>
`);

export const TRANSACTIONS_TEMPLATE = compile(`
<div class="transactions-container">
  <table class="transactions-table font-family-monospace">
  {{# each transactions}}
    <tr>
      <td class="px-2 date">
        {{date}}
      </td>
      <td class="px-2 amount {{sign amount}} text-right border-left border-dark">
        {{amount}}
      </td>
      <td class="account-{{account}} border-left border-right border-dark">
      </td>
    </tr>
  {{/ each}}
  {{# each metrics}}
    {{# each metrics}}
      <tr>
        {{# if @first}}
          <td class="px-2 date text-center border-top border-dark" rowspan="3">
            {{../period}}
          </td>
        {{/ if}}
        <td class="px-2 amount {{sign amount}} text-right {{# if @first}} border-top {{/ if}} border-left border-dark">
          {{amount}}
        </td>
        <td class="{{# if @first}} border-top {{/ if}} border-left border-right border-dark">
        </td>
      </tr>
    {{/ each}}
  {{/ each}}
  </table>
  <div class="scroll-window">
    <table class="transactions-table font-family-monospace">
      {{# each transactions}}
        <tr>
          <td class="px-2">
            <span class="description">
              {{clean_description}}
            </span>
            {{#if tag}}
              <span id="tag-{{@index}}" class="ml-2 p-1 tag tag-{{concat tag}} font-family-sans-serif font-size-tiny">
                {{tag}}
              </span>
            {{/if}}
          </td>
          <td id="copy-button-{{@index}}" class="px-2 copy-button">
            <span class="fas fa-clone font-size-small"></span>
          </td>
        </tr>
      {{/ each}}
      {{# each metrics}}
        {{# each metrics}}
          <tr>
            <td class="px-2 description {{# if @first}} border-top border-dark {{/ if}}" colspan="2">
              {{description}}
            </td>
          </tr>
        {{/ each}}
      {{/ each}}
    </table>
  </div>
</div>
`);
